# -*- coding: utf-8 -*-
"""Aba ENTREVISTA da ficha do cliente (produtor rural, defesa contra bancos).

O modal "Ficha do cliente" do chat ao vivo tem 7 campos genericos e um campo de
Anotacoes. A entrevista do produtor rural nao cabe ali: sao ~50 perguntas (producao,
credito e banco, garantias, perda de safra, pedido ao banco, cobranca). Esta
aba poe cada pergunta em um campo de verdade, para o juridico depois EXTRAIR
resposta por resposta em vez de garimpar texto solto.

DESENHO
- Tabela propria `ficha_entrevista`, chave/valor: (conversa_id, campo, valor).
  Acrescentar pergunta depois nao exige migracao nem repatch do frontend.
- O ESQUEMA das perguntas mora AQUI. O frontend so desenha o que este endpoint
  devolve, entao mudar pergunta e editar este arquivo.
- Router e tabela NOVOS. Nao encosta em `atendimento.py`, no modelo `Conversa`
  nem em nenhum fluxo existente.

TRANSCRICAO
O time pode anexar aqui o arquivo da transcricao. Ele vai para a mesma pasta do
lead no Drive que o `subir-drive` ja usa (`drive_leads`), com o nome do cliente
no arquivo, que e por onde o `transcricao_drive.py` procura.
Atencao de quem for mexer: ligacao feita PELO RAMAL ja e gravada e transcrita
sozinha pelo `transcrever_ligacoes.py` (cron 1/min) e anexada na conversa. Este
anexo e o plano B, para ligacao feita fora do ramal.
"""
import io
import re
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import usuario_atual
from ..database import get_db, Usuario

router = APIRouter(prefix='/api/ficha-entrevista', tags=['ficha-entrevista'])

MAX_ANEXO = 20 * 1024 * 1024          # 20 MB
EXT_OK = ('.txt', '.md', '.docx', '.doc', '.pdf', '.rtf', '.odt')


def _c(cid, label, tipo='texto', obrig=False, opcoes=None):
    d = {'id': cid, 'label': label, 'tipo': tipo}
    if obrig:
        d['obrigatorio'] = True
    if opcoes:
        d['opcoes'] = opcoes
    return d


# --- O esquema. Cada bloco vira um titulo; cada campo, um input. -------------
# tipo: 'texto' (uma linha) | 'area' (varias linhas) | 'opcao' (select)
BLOCOS = [
    # Bloco do CLIENTE: o endereco preenchido AQUI vale como comprovante para a contratacao
    # avancar (o vigia le o campo 'endereco_cliente'; o arquivo do comprovante e cobrado depois,
    # na organizacao de documentos). Fluxo: fechou na ligacao -> pede o documento -> preenche o
    # endereco na entrevista -> contrato sai.
    {'id': 'cliente', 'titulo': 'O produtor',
     'ajuda': 'Endereco completo aqui libera o contrato sem esperar o arquivo do '
              'comprovante. Anote como ele falar: rua ou estrada, numero ou km, bairro ou '
              'comunidade, cidade e CEP. Casado: o conjuge assina junto quando ha garantia real.',
     'campos': [
         _c('endereco_cliente', 'Endereco completo do cliente (rua/estrada, numero/km, bairro, cidade e CEP)',
            'area', True),
         _c('estado_civil_regime', 'Estado civil e regime de bens', obrig=True),
         _c('conjuge', 'Nome e CPF do conjuge (se casado ou uniao estavel)'),
         _c('pessoa_juridica', 'Produz como pessoa fisica ou tem empresa rural (CNPJ)?'),
     ]},
    {'id': 'producao', 'titulo': 'A producao',
     'ajuda': 'O tamanho e o tipo de producao mudam a linha de credito (Pronaf, Pronamp, '
              'demais) e a defesa da terra. Pergunte em hectares; se ele falar em alqueire, anote '
              'como falou.',
     'campos': [
         _c('atividade', 'O que planta ou cria (cultura, rebanho, leite...)', obrig=True),
         _c('area_total', 'Area total (ha) e quanto e plantado/ocupado', obrig=True),
         _c('posse_terra', 'Terra propria, arrendada ou em parceria', 'opcao', True,
            ['', 'Propria', 'Arrendada', 'Parceria', 'Mista']),
         _c('modulos_fiscais', 'Pequena propriedade (ate 4 modulos fiscais) tocada pela familia?', 'opcao', True,
            ['', 'Sim, familia trabalha nela', 'Nao', 'Nao sabe']),
         _c('imovel_matricula', 'Nome do imovel, municipio e numero da matricula'),
         _c('mora_no_imovel', 'Mora no imovel? E a unica propriedade da familia?'),
         _c('dap_caf', 'Tem DAP ou CAF (agricultura familiar)?', 'opcao', False,
            ['', 'Sim', 'Nao', 'Vencida', 'Nao sabe']),
         _c('produtividade', 'Produtividade normal x produtividade da safra ruim (sc/ha, @, litros)', 'area'),
     ]},
    {'id': 'credito', 'titulo': 'O credito e o banco', 'campos': [
        _c('razao_social', 'Banco ou cooperativa credora (razao social completa)', obrig=True),
        _c('cnpj', 'CNPJ do banco/cooperativa'),
        _c('agencia_gerente', 'Agencia, cidade e nome do gerente'),
        _c('linhas', 'Quais operacoes: custeio, investimento, Pronaf, Pronamp, Funcafe, CPR, CCB, '
                     'capital de giro (numero e data de cada cedula)', 'area', True),
        _c('valor_contratado', 'Valor contratado em cada operacao (R$)', 'area', True),
        _c('saldo_devedor', 'Saldo devedor hoje, segundo o banco (R$)', obrig=True),
        _c('vencimentos', 'Vencimentos: parcela vencida e proximas (datas)', 'area', True),
        _c('taxa_encargos', 'Taxa de juros e encargos que o banco cobra (e se mudou)'),
        _c('venda_casada', 'Teve venda casada? Seguro, capitalizacao, consorcio, previdencia'),
        _c('renegociacoes', 'Ja renegociou ou repactuou antes? Quantas vezes e o que mudou', 'area'),
        _c('outros_bancos', 'Deve para outros bancos, cooperativas, tradings ou revendas? Quanto'),
    ]},
    {'id': 'garantias', 'titulo': 'Garantias',
     'ajuda': 'A garantia define o risco: hipoteca e alienacao fiduciaria levam a leilao; penhor '
              'e alienacao de maquina levam a busca e apreensao.',
     'campos': [
         _c('tipo_garantia', 'Garantia dada', 'opcao', True,
            ['', 'Hipoteca', 'Alienacao fiduciaria do imovel', 'Penhor de safra', 'Penhor de maquinas',
             'Penhor de gado', 'Alienacao fiduciaria de maquina/veiculo', 'Aval', 'Mais de uma']),
         _c('bens_garantia', 'Quais bens estao em garantia (imovel, maquinas, gado, safra)', 'area', True),
         _c('avalistas', 'Avalistas ou fiadores (nome e parentesco)'),
     ]},
    {'id': 'perda', 'titulo': 'O que aconteceu com a safra',
     'ajuda': 'Prorrogacao depende de prova da frustracao ou da dificuldade de venda. ANOTE O QUE '
              'EXISTE E O QUE NAO EXISTE.',
     'campos': [
         _c('evento', 'O que aconteceu', 'opcao', True,
            ['', 'Seca/estiagem', 'Geada', 'Excesso de chuva', 'Granizo', 'Praga/doenca',
             'Queda de preco', 'Doenca no rebanho', 'Outro', 'Nada (so a parcela nao fecha)']),
         _c('evento_detalhe', 'Quando foi e quanto perdeu (% da producao, sacas, R$)', 'area', True),
         _c('laudo', 'Tem laudo agronomico ou tecnico da perda? De quem', obrig=True),
         _c('proagro_seguro', 'Acionou Proagro ou seguro rural? Resultado'),
         _c('decreto_emergencia', 'O municipio decretou emergencia ou calamidade? Quando'),
         _c('notas_venda', 'Tem notas fiscais de produtor da safra boa e da safra ruim?'),
     ]},
    {'id': 'banco', 'titulo': 'Pedido ao banco',
     'ajuda': 'Pedido de prorrogacao feito ANTES do vencimento e POR ESCRITO pesa muito. '
              'Anote a resposta do banco literal.',
     'campos': [
         _c('pediu_prorrogacao', 'Pediu prorrogacao ou alongamento ao banco?', 'opcao', True,
            ['', 'Sim, por escrito', 'Sim, so de boca', 'Nao']),
         _c('data_pedido', 'Quando pediu (antes ou depois do vencimento)'),
         _c('resposta_banco', 'O que o banco respondeu (ANOTAR LITERAL)', 'area', True),
         _c('exigencias_banco', 'O banco exigiu algo para renegociar (entrada, nova garantia, seguro)'),
     ]},
    {'id': 'cobranca', 'titulo': 'Situacao da cobranca: define a urgencia', 'campos': [
        _c('situacao', 'Situacao hoje', 'opcao', True,
           ['', 'Em dia / a vencer', 'Vencida sem cobranca judicial', 'Negativado', 'Execucao na Justica',
            'Leilao marcado', 'Busca e apreensao', 'Consolidacao da propriedade (alienacao fiduciaria)']),
        _c('data_urgente', 'Data do leilao, da citacao ou do mandado', obrig=True),
        _c('processo_numero', 'Numero do processo (se houver)'),
        _c('penhora_bloqueio', 'Teve penhora ou bloqueio de conta? Quanto'),
        _c('notificacoes', 'Recebeu notificacao ou carta do banco? Quando', 'area'),
        _c('advogado_anterior', 'Ja teve advogado nesse caso', obrig=True),
    ]},
    {'id': 'documentos', 'titulo': 'Documentos que ele tem',
     'ajuda': 'ANOTE AS NEGATIVAS. Se ele disser que NAO tem, escreva. E o que impede a cobranca '
              'automatica de pedir o que nao existe.',
     'campos': [
         _c('tem_cedulas', 'Tem as cedulas/contratos do banco (copias)?'),
         _c('tem_extratos', 'Tem extratos ou planilha de evolucao da divida?'),
         _c('tem_matricula_ccir', 'Tem matricula do imovel, CCIR, ITR e CAR?'),
         _c('tem_projeto', 'Tem o orcamento/projeto tecnico do financiamento?'),
         _c('negativas', 'NEGATIVAS expressas (nao tem laudo, nao pediu por escrito, etc.)', 'area', True),
     ]},
]

# Todo bloco ganha um campo de observacao proprio, no fim.
for _b in BLOCOS:
    _b['campos'].append(_c(f"obs_{_b['id']}", 'Observacao', 'area'))

CAMPOS_VALIDOS = {c['id'] for b in BLOCOS for c in b['campos']}
OBRIGATORIOS = [c['id'] for b in BLOCOS for c in b['campos'] if c.get('obrigatorio')]

DDL = """
create table if not exists ficha_entrevista (
  id integer primary key autoincrement,
  conversa_id integer not null,
  campo varchar(60) not null,
  valor text,
  atualizado_em datetime,
  atualizado_por varchar(200)
);
create unique index if not exists ux_ficha_entrevista
  on ficha_entrevista (conversa_id, campo);
"""


async def _garantir_tabela(db: AsyncSession):
    for comando in DDL.strip().split(';'):
        if comando.strip():
            await db.execute(text(comando))


class RespostasReq(BaseModel):
    respostas: dict


@router.get('/campos')
async def campos(user: Usuario = Depends(usuario_atual)):
    """O esquema das perguntas. O frontend desenha a partir daqui."""
    return {'blocos': BLOCOS, 'obrigatorios': OBRIGATORIOS}


@router.get('/{conversa_id}')
async def ler(conversa_id: int, user: Usuario = Depends(usuario_atual),
              db: AsyncSession = Depends(get_db)):
    await _garantir_tabela(db)
    linhas = (await db.execute(
        text('select campo, valor from ficha_entrevista where conversa_id=:c'),
        {'c': conversa_id})).fetchall()
    respostas = {campo: valor for campo, valor in linhas}
    faltando = [c for c in OBRIGATORIOS if not (respostas.get(c) or '').strip()]
    return {'ok': True, 'conversa_id': conversa_id, 'respostas': respostas,
            'faltando': faltando, 'total_obrigatorios': len(OBRIGATORIOS)}


@router.put('/{conversa_id}')
async def gravar(conversa_id: int, req: RespostasReq,
                 user: Usuario = Depends(usuario_atual),
                 db: AsyncSession = Depends(get_db)):
    """Grava so os campos do esquema. Campo desconhecido e ignorado de proposito.

    NAO toca em wa_conversas: `atualizado_em` de la e lido pela fila da vendedora
    e pelos relatorios como 'ultima atividade do lead', e preencher ficha nao e
    atividade do lead.
    """
    await _garantir_tabela(db)
    agora = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    gravados = 0
    for campo, valor in (req.respostas or {}).items():
        if campo not in CAMPOS_VALIDOS:
            continue
        await db.execute(text(
            'insert into ficha_entrevista (conversa_id, campo, valor, atualizado_em, atualizado_por) '
            'values (:c, :k, :v, :t, :u) '
            'on conflict(conversa_id, campo) do update set '
            'valor=excluded.valor, atualizado_em=excluded.atualizado_em, '
            'atualizado_por=excluded.atualizado_por'),
            {'c': conversa_id, 'k': campo, 'v': (valor or ''), 't': agora, 'u': user.email})
        gravados += 1
    await db.commit()
    linhas = (await db.execute(
        text('select campo, valor from ficha_entrevista where conversa_id=:c'),
        {'c': conversa_id})).fetchall()
    respostas = {c: v for c, v in linhas}
    faltando = [c for c in OBRIGATORIOS if not (respostas.get(c) or '').strip()]
    return {'ok': True, 'gravados': gravados, 'faltando': faltando}


@router.post('/{conversa_id}/transcricao')
async def anexar_transcricao(conversa_id: int, arquivo: UploadFile = File(...),
                             user: Usuario = Depends(usuario_atual),
                             db: AsyncSession = Depends(get_db)):
    """Sobe o arquivo da transcricao para a pasta do lead no Google Drive.

    Nome do arquivo leva o NOME DO CLIENTE, porque e por ele que o
    `transcricao_drive.py` procura (busca por token do nome, nao por substring).
    """
    nome_arq = (arquivo.filename or 'transcricao.txt')
    if not nome_arq.lower().endswith(EXT_OK):
        raise HTTPException(400, f'Formato nao aceito. Use: {", ".join(EXT_OK)}')
    dados = await arquivo.read()
    if not dados:
        raise HTTPException(400, 'Arquivo vazio')
    if len(dados) > MAX_ANEXO:
        raise HTTPException(400, f'Arquivo maior que {MAX_ANEXO // (1024*1024)} MB')

    linha = (await db.execute(text(
        'select contato_nome, contato_telefone, drive_pasta_id from wa_conversas where id=:c'),
        {'c': conversa_id})).fetchone()
    if not linha:
        raise HTTPException(404, 'Conversa nao encontrada')
    nome_lead, telefone, pasta_id = linha[0] or '', linha[1] or '', linha[2] or ''
    if not nome_lead.strip():
        raise HTTPException(400, 'A conversa nao tem NOME do cliente. Preencha o nome na '
                                 'aba Ficha antes de anexar: a esteira procura a transcricao '
                                 'pelo nome do arquivo.')

    ext = '.' + nome_arq.rsplit('.', 1)[-1].lower()
    limpo = re.sub(r'[^\w\s-]', '', nome_lead).strip()[:60] or 'cliente'
    destino = f"Transcricao {limpo} {datetime.now().strftime('%Y-%m-%d')}{ext}"

    import sys
    sys.path.insert(0, '/opt/escritorio/INTEGRACOES')
    try:
        from google_integration import autenticar_google
        from googleapiclient.http import MediaIoBaseUpload
        from ..whatsapp import drive_leads
        drive, _ = autenticar_google()
        if pasta_id:
            pasta = {'id': pasta_id, 'url': ''}
        else:
            pasta = drive_leads.resolver_pasta_lead(drive, nome_lead, telefone)
        midia = MediaIoBaseUpload(io.BytesIO(dados), mimetype='application/octet-stream',
                                  resumable=False)
        criado = drive.files().create(
            body={'name': destino, 'parents': [pasta['id']]},
            media_body=midia, fields='id, webViewLink',
            supportsAllDrives=True).execute()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f'Falha ao subir para o Drive: {e}')

    link = criado.get('webViewLink', '')
    await _garantir_tabela(db)
    agora = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    await db.execute(text(
        'insert into ficha_entrevista (conversa_id, campo, valor, atualizado_em, atualizado_por) '
        'values (:c, :k, :v, :t, :u) on conflict(conversa_id, campo) do update set '
        'valor=excluded.valor, atualizado_em=excluded.atualizado_em, '
        'atualizado_por=excluded.atualizado_por'),
        {'c': conversa_id, 'k': '_transcricao_link', 'v': link, 't': agora, 'u': user.email})
    if not pasta_id and pasta.get('id'):
        await db.execute(text('update wa_conversas set drive_pasta_id=:p where id=:c'),
                         {'p': pasta['id'], 'c': conversa_id})
    await db.commit()
    return {'ok': True, 'arquivo': destino, 'link': link}
