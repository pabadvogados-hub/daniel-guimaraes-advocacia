# -*- coding: utf-8 -*-
"""FLUXO "A DIVIDA JA VENCEU?" do Guimarães Advocacia (nome do arquivo herdado: fluxo_saiu).

Produtor rural que estava com a divida EM DIA, ou nunca disse, quando falou com a gente recebe UMA
mensagem escrita so para ele (mensagem_personalizada.py) perguntando como esta a divida: em dia, ou
ja venceu e o banco esta cobrando (execucao, leilao, busca e apreensao).
Quem responde que JA ESTA EM COBRANCA vira QUENTISSIMO e o vendedor da vez recebe na hora um
LIGAR AGORA com o caso (roteamento_vendedoras.py, equipe em VENDEDORES no .env). Sem vendedor
cadastrado, o aviso vai para FLUXO_SAIU_RESUMO.

CODIGOS HERDADOS (mantidos porque termometro e painel comercial leem esses valores):
  'saiu'        = divida ja em cobranca (vencida, negativada, execucao, leilao, apreensao)
  'trabalhando' = divida em dia / a vencer

REVISITA: quem respondeu que ESTA EM DIA recebe a pergunta de novo 60 dias depois da resposta,
porque safra ruim e preco baixo mudam a situacao de uma estacao para outra.

Regras:
- do contato MAIS ANTIGO para o mais novo
- 30 por dia, no maximo 3 por minuto; aqui sai 1 por rodada do cron, espacado
- dia util, das 9h as 18h
- fora: cliente, Perdido/Desqualificado, contrato, sem caso, ja tem acao, pediu para parar,
  nunca escreveu, conversa ativa nos ultimos 3 dias
- uma mensagem so; sem resposta, nao insiste
- quem esta em dia NAO e tratado como caso perdido (a revisita existe)

.env: FLUXO_SAIU_RESUMO (telefone que recebe o resumo e as copias; vazio = nao envia).

  --fila N      mostra os proximos N da fila, sem escrever nem enviar
  --enviar      envia o proximo da fila (respeita teto do dia, janela e ritmo)
  --varrer      le as respostas e age (quentissimo + vendedor, trabalhando, parar)
  --resumo      manda o resumo do dia para FLUXO_SAIU_RESUMO
  --teste FONE  escreve as mensagens dos 3 proximos da fila e manda para FONE
"""
import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mensagem_personalizada as MP  # noqa: E402
import roteamento_vendedoras as ROTA  # noqa: E402
import wa_dapi  # noqa: E402  (saida unica de WhatsApp: D-API)

load_dotenv('/opt/escritorio/config/.env')
load_dotenv('/opt/escritorio/config/.env', override=False)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB = '/opt/escritorio/SISTEMA/backend/sistema_esc.db'
ESTADO = '/opt/escritorio/SYNC/fluxo_saiu_state.json'
RESUMO_TEL = os.getenv('FLUXO_SAIU_RESUMO') or os.getenv('TEL_ALERTA_EQUIPE', '')     # quem recebe o resumo do dia e as copias dos avisos
TETO_DIA = 30
JANELA = (9, 18)
MIN_ENTRE_ENVIOS = 20            # segundos: nunca mais de 3 por minuto
FORA_ETAPA = ('Perdido', 'Perdido - Sem resposta', 'Perdido - Sem interesse', 'Lead Desqualificado',
              'Novo Cliente', 'Contrato / Assinatura', 'Assinado', 'Contrato no ZapSign')
REVISITA_DIAS = int(os.getenv('FLUXO_REVISITA_DIAS', '60'))   # quem disse "esta em dia" volta depois disso


def agora_br():
    return datetime.utcnow() - timedelta(hours=3)


def sa(s):
    return ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower()) if unicodedata.category(c) != 'Mn')


def t8(x):
    return ''.join(c for c in str(x or '') if c.isdigit())[-8:]


def dt(s):
    return datetime.strptime(str(s).replace('T', ' ').split('.')[0], '%Y-%m-%d %H:%M:%S')


JA_TEM = re.compile(r'(ja (tenho|to com|estou com|contratei) (um |uma )?advogad|ja (entrei|abri|dei entrada|processei)|'
                    r'ja (tenho|tem) (um |uma )?(processo|acao)|ja com outro advogad)')
PARE = re.compile(r'(nao (me )?(mande|manda|envie) mais|para de (me )?mandar|me tira|sai(r)? da lista|'
                  r'nao tenho interesse|nao quero mais|bloque)')
# Nome herdado (TRABALHISTA): aqui e o filtro de ASSUNTO do produtor rural / divida rural.
TRABALHISTA = re.compile(r'(produtor|agricult|pecuar|fazend|sitio|lavoura|safra|plantio|colheita|soja|milho|'
                         r'cafe|gado|rebanho|hectare|alqueire|credito rural|custeio|pronaf|pronamp|funcafe|cpr|'
                         r'cedula|banco|cooperativa|prorroga|alonga|renegoci|divida|parcela|leilao|execucao|'
                         r'busca e apreensao|trator|maquina|negativad|seca|geada|proagro)')
# Mesma logica de app/whatsapp/coluna_lead.py (copiada de proposito: o backend nao importa o SYNC).
# 'trabalhando' = em dia; 'saiu' = ja em cobranca.
NEGOU = re.compile(r'(nao venceu|ainda nao venceu|nao esta vencid|nao ta vencid|nunca atrasei|'
                   r'nao tem execucao|nao tem leilao|nao entraram na justica|nao entrou na justica)')
SAIU = re.compile(r'(venceu|vencid|atrasad|atrasei|em atraso|nao consegui pagar|nao paguei|deixei de pagar|'
                  r'negativad|nome sujo|serasa|spc|protest|cobranca judicial|entrou na justica|'
                  r'entraram na justica|me processou|me executando|execucao|executad|leilao|leiloar|'
                  r'busca e apreensao|apreend|tomaram|vao tomar|consolidac|penhor(a|aram)|bloque(io|aram))')
FICOU = re.compile(r'(to em dia|estou em dia|esta em dia|ta em dia|pago em dia|vence (so )?(em|no|na|mes|ano)|'
                   r'vai vencer|ainda vai vencer|a vencer|antes de vencer|ainda nao venceu|consegui pagar|paguei)')


# ------------------------------------------------------------------ estado
def carregar():
    try:
        with open(ESTADO, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {'enviados': {}, 'nao_contatar': [], 'dias': {}}


def salvar(e):
    tmp = ESTADO + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(e, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ESTADO)


# ------------------------------------------------------------------ fila
def fila(con, estado):
    cli = {t8(t) for a, b in con.execute('select telefone, celular from jur_clientes') for t in (a, b)
           if t and len(t8(t)) == 8}
    nao = set(map(str, estado['nao_contatar']))
    # revisita: disse "esta em dia" ha REVISITA_DIAS ou mais (no maximo 2 revisitas por pessoa)
    corte = (agora_br() - timedelta(days=REVISITA_DIAS)).strftime('%Y-%m-%d %H:%M')
    revisitar = {k: v for k, v in estado['enviados'].items()
                 if v.get('resultado') == 'trabalhando' and (v.get('respondeu_em') or '9999') <= corte
                 and len(v.get('anteriores', [])) < 2 and k not in nao}
    ja = (set(estado['enviados']) - set(revisitar)) | nao
    saida = []
    rows = con.execute(
        "select v.id, v.contato_nome, v.contato_telefone, v.etapa, v.criado_em, "
        "       coalesce(t.situacao,''), coalesce(t.temperatura,''), coalesce(v.e_reclamante,0) "
        "  from wa_conversas v left join lead_termometro t on t.conversa_id=v.id "
        " where v.pipeline_id=10 order by v.criado_em asc").fetchall()
    for cid, nome, tel, etapa, criado, sit, temp, e_cam in rows:
        if str(cid) in ja or sit == 'saiu' or temp == 'sem_caso' or etapa in FORA_ETAPA:
            continue
        if not tel or len(t8(tel)) < 8 or t8(tel) in cli:
            continue
        deles = [r[0] or '' for r in con.execute(
            "select conteudo from wa_mensagens where conversa_id=? and origem='contato' order by id desc limit 10",
            (cid,))]
        if not deles:
            continue
        txt = sa(' '.join(deles))
        if JA_TEM.search(txt) or PARE.search(txt):
            continue
        # so entra quem tem sinal de divida rural (o quadro tem vendedor, engano, outros assuntos)
        if not e_cam and not TRABALHISTA.search(txt):
            continue
        ult = con.execute("select max(criado_em) from wa_mensagens where conversa_id=?", (cid,)).fetchone()[0]
        if ult and datetime.utcnow() - dt(ult) < timedelta(days=3):
            continue
        saida.append({'id': cid, 'nome': nome, 'tel': tel, 'criado': criado, 'sit': sit or 'nao_informado',
                      'temp': temp, 'revisita': str(cid) in revisitar, 'antes': revisitar.get(str(cid))})
    saida.sort(key=lambda x: not x['revisita'])      # revisita primeiro; o resto segue do mais antigo
    return saida


# ------------------------------------------------------------------ envio
def zapi(fone, texto):
    # Canal: D-API pelo numero oficial (wa_dapi). ok so quando a D-API confirmou o envio.
    if not ''.join(ch for ch in str(fone or '') if ch.isdigit()):
        return False, 'sem destino configurado'
    try:
        ok, info = wa_dapi.enviar_texto(fone, texto)
    except Exception as e:          # sem credencial D-API: conta como envio que falhou
        return False, ('%s: %s' % (type(e).__name__, e))[:160]
    return ok, json.dumps(info, ensure_ascii=False)[:160]


def no_horario(vend, a=None):
    """O vendedor so recebe WhatsApp da API no horario dele (dia util)."""
    a = a or agora_br()
    h = vend.get('horas', JANELA)
    return a.weekday() in vend.get('dias', (0, 1, 2, 3, 4)) and h[0] <= a.hour < h[1]


def avisar_vendedora(cid, v, vend, aviso):
    """No horario dela, o aviso vai pelo WhatsApp. Fora dele, so a tarefa fixa na tela, com a mesma
    referencia do alarme (ligar-agora:<codigo>), para o mesmo lead nunca virar duas tarefas."""
    if no_horario(vend):
        ok, _ = zapi(vend['tel'], aviso)
        return ok
    import io
    _saida, sys.stdout = sys.stdout, io.StringIO()   # mesmo cuidado do lead_quente_tarefa com o stdout
    try:
        import lead_quente_tarefa as LQ
    finally:
        sys.stdout = _saida
    tid = LQ.gravar({'vend': vend['nome'], 'origem': 'ligar-agora', 'ref': 'ligar-agora:%s' % cid,
                     'titulo': 'LIGAR AGORA: %s · %s' % (v['nome'] or 'Sem nome', v['tel']),
                     'texto': LQ._limpo(aviso) + '\n\nDepois da ligação, atualize o card no CRM e conclua '
                              'esta tarefa.',
                     'nome': v['nome'] or '', 'tel': v['tel'], 'cid': int(cid)})
    v['tarefa_fora_do_horario'] = tid
    print('   fora do horario de %s: sem WhatsApp, tarefa #%s na tela' % (vend['nome'], tid))
    return False


def pode_enviar(estado):
    a = agora_br()
    if a.weekday() >= 5 or not (JANELA[0] <= a.hour < JANELA[1]):
        return False, 'fora da janela (dia util, %dh as %dh)' % JANELA
    hoje = a.strftime('%Y-%m-%d')
    if estado['dias'].get(hoje, 0) >= TETO_DIA:
        return False, 'teto do dia atingido (%d)' % TETO_DIA
    ultimo = max((v.get('enviado_ts', 0) for v in estado['enviados'].values()), default=0)
    if time.time() - ultimo < MIN_ENTRE_ENVIOS:
        return False, 'aguardando intervalo minimo entre envios'
    return True, ''


def enviar_proximo():
    estado = carregar()
    ok, motivo = pode_enviar(estado)
    if not ok:
        print(motivo)
        return
    con = sqlite3.connect('file:%s?mode=ro' % DB, uri=True, timeout=20)
    for lead in fila(con, estado)[:3]:           # tenta ate 3, caso a mensagem nao passe na conferencia
        ctx = MP.contexto(con, lead['id'])
        if lead.get('revisita'):
            ctx['revisita'] = {'quando': (lead['antes'].get('respondeu_em') or '')[:10],
                               'resposta': lead['antes'].get('resposta') or ''}
        msg, prob = MP.escrever(ctx)
        if prob == 'nao_e_lead':
            estado['nao_contatar'].append(lead['id'])      # a IA leu e viu que nao e lead de produtor rural
            estado.setdefault('nao_e_lead', []).append({'id': lead['id'], 'nome': lead['nome']})
            salvar(estado)
            print('#%d nao e lead de produtor rural, fora da fila: %s' % (lead['id'], lead['nome']))
            continue
        if prob == 'llm_indisponivel':
            # sem IA o fluxo para em silencio: avisa FLUXO_SAIU_RESUMO uma vez por dia
            hoje = agora_br().strftime('%Y-%m-%d')
            if estado.get('avisou_llm') != hoje:
                estado['avisou_llm'] = hoje
                salvar(estado)
                zapi(RESUMO_TEL, 'ATENÇÃO: o fluxo "a dívida já venceu?" parou: a IA não está respondendo, nem pela chave da '
                          'API nem pelo Claude do servidor. Nenhuma mensagem foi enviada. Precisa olhar.')
            print('#%d nao enviado: a IA nao respondeu' % lead['id'])
            return
        if prob:
            print('#%d pulado hoje: %s' % (lead['id'], prob))
            continue
        ok, resp = zapi(lead['tel'], msg)
        hoje = agora_br().strftime('%Y-%m-%d')
        if ok:
            anteriores = []
            velho = estado['enviados'].get(str(lead['id']))
            if velho and lead.get('revisita'):              # guarda a rodada anterior, nao apaga historico
                anteriores = velho.get('anteriores', []) + [
                    {k: velho.get(k) for k in ('enviado', 'mensagem', 'resultado', 'resposta', 'respondeu_em')}]
            estado['enviados'][str(lead['id'])] = {
                'tel': lead['tel'], 'nome': lead['nome'], 'enviado': agora_br().strftime('%Y-%m-%d %H:%M'),
                'enviado_ts': time.time(), 'enviado_utc': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'situacao_antes': lead['sit'], 'contato_desde': str(lead['criado'])[:10],
                'mensagem': msg, 'resultado': '', 'revisita': bool(lead.get('revisita')),
                'anteriores': anteriores}
            estado['dias'][hoje] = estado['dias'].get(hoje, 0) + 1
            salvar(estado)
            print('ENVIADO #%d %s (desde %s)%s | hoje: %d/%d'
                  % (lead['id'], lead['nome'], str(lead['criado'])[:10],
                     ' REVISITA' if lead.get('revisita') else '', estado['dias'][hoje], TETO_DIA))
        else:
            print('FALHOU o envio para #%d: %s' % (lead['id'], resp))
        break
    con.close()


# ------------------------------------------------------------------ volta
def classificar(texto, usar_ia=True):
    t = ' '.join(sa(texto).split())
    if PARE.search(t):
        return 'parar'
    if NEGOU.search(t) or FICOU.search(t):
        return 'trabalhando'
    if SAIU.search(t):
        return 'saiu'
    if usar_ia and len(t.split()) >= 2:
        return classificar_ia(texto)
    return 'outro'


def classificar_ia(texto):
    """Resposta que a regra nao entendeu: a IA le e responde com uma palavra so."""
    pedido = ('Um produtor rural recebeu a pergunta "a divida com o banco ainda esta em dia ou ja venceu e o '
              'banco esta cobrando?" e respondeu:\n\n"%s"\n\nResponda com UMA palavra: saiu (se a divida ja '
              'venceu, esta negativado, ou ha execucao, leilao ou busca e apreensao), trabalhando (se esta em dia '
              'ou ainda vai vencer), parar (se pediu para nao receber mais mensagem) ou outro (se nao da para saber).'
              % texto[:600])
    try:
        saida = MP.chamar(pedido, modelo=MP.MODELO_LEITURA, max_tokens=16)
        w = sa(saida.strip().split()[0]) if saida.strip() else ''
        return w if w in ('saiu', 'trabalhando', 'parar') else 'outro'
    except Exception:
        return 'outro'


def varrer():
    estado = carregar()
    pend = {k: v for k, v in estado['enviados'].items() if not v.get('resultado')}
    if not pend:
        return
    con = sqlite3.connect(DB, timeout=30)      # precisa escrever: termometro, etapa e nota
    for cid, v in pend.items():
        falas = [r[0] or '' for r in con.execute(
            "select conteudo from wa_mensagens where conversa_id=? and origem='contato' and criado_em > ? "
            "order by id", (int(cid), v['enviado_utc']))]
        if not falas:
            continue
        resposta = ' '.join(' '.join(f.split()) for f in falas)
        tipo = classificar(resposta)
        if tipo == 'outro':
            v['resposta_vista'] = resposta[:300]
            continue
        v['resultado'] = tipo
        v['resposta'] = resposta[:400]
        v['respondeu_em'] = agora_br().strftime('%Y-%m-%d %H:%M')
        ult = con.execute('select max(id) from wa_mensagens where conversa_id=?', (int(cid),)).fetchone()[0]
        if tipo == 'saiu':
            vend = ROTA.quem_recebe_demitido()         # rodizio entre os vendedores em horario (ou None)
            con.execute("update lead_termometro set situacao='saiu', temperatura='quentissimo', ultima_msg_id=? "
                        " where conversa_id=?", (ult, int(cid)))
            # sobe de etapa no quadro, mas nunca rebaixa quem ja avancou
            con.execute("update wa_conversas set etapa='Lead Quente', atualizado_em=? where id=? "
                        " and etapa in ('Caixa de Entrada','Campanha Prorrogação','Campanha Execução e Leilão',"
                        "'Campanha Busca e Apreensão','Campanha Geral','Contatado','Em Qualificação','')",
                        (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), int(cid)))
            con.execute("insert into wa_mensagens (conversa_id, origem, autor, tipo, conteudo, midia_url, "
                        " criado_em) values (?,?,?,?,?,'',?)",
                        (int(cid), 'nota', 'fluxo:saiu', 'texto',
                         '[FLUXO] Respondeu que a dívida já está em cobrança. Virou lead quentíssimo, foi para Lead Quente '
                         'e %s foi avisado(a) para ligar agora.' % (vend['nome'] if vend else 'o time'),
                         datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
            con.commit()
            r = con.execute('select resumo, violacoes from lead_termometro where conversa_id=?',
                            (int(cid),)).fetchone() or ('', '')
            d = ''.join(c for c in v['tel'] if c.isdigit())
            aviso = ('*LIGAR AGORA · acabou de dizer que a dívida está em cobrança*\n\n*%s*\nhttps://wa.me/%s\n\n'
                     'Respondeu agora: "%s"\n\nO caso: %s\n\nFalou com a gente pela primeira vez em %s.\n\n'
                     '*É agora que ele decide.* Quem avisa que o banco está cobrando e não recebe ligação no mesmo '
                     'dia esfria e acaba procurando outro escritório, e o prazo da execução ou do leilão segue '
                     'correndo. Leia a conversa antes de ligar.'
                     % (v['nome'] or 'Sem nome', d, resposta[:200], (r[0] or '-')[:300], v['contato_desde']))
            ok = avisar_vendedora(cid, v, vend, aviso) if vend else False   # fora do horario: so a tarefa fixa
            time.sleep(2)
            ok2, _ = zapi(RESUMO_TEL, aviso + ('\n\nFoi para *%s*.' % vend['nome'] if vend else ''))   # copia
            v['vendedora'] = vend['nome'] if vend else ''
            v['vendedora_avisada'] = ok
            v['pam_avisada'] = ok2
        elif tipo == 'trabalhando':
            con.execute("update lead_termometro set situacao='trabalhando', ultima_msg_id=? where conversa_id=?",
                        (ult, int(cid)))
            con.commit()
        elif tipo == 'parar':
            estado['nao_contatar'].append(int(cid))
        print('#%s %s -> %s' % (cid, v['nome'], tipo))
    con.close()
    salvar(estado)


def resumo():
    estado = carregar()
    hoje = agora_br().strftime('%Y-%m-%d')
    env = [v for v in estado['enviados'].values() if v['enviado'].startswith(hoje)]
    tudo = list(estado['enviados'].values())
    saiu = [v for v in tudo if v.get('resultado') == 'saiu' and (v.get('respondeu_em') or '').startswith(hoje)]
    L = ['*Fluxo "a dívida já venceu?"* · %s' % agora_br().strftime('%d/%m'),
         'Enviadas hoje: %d | no total: %d' % (len(env), len(tudo)),
         'Responderam no total: %d' % sum(1 for v in tudo if v.get('resultado') or v.get('resposta_vista')),
         '  em cobrança: %d · em dia: %d · pediram para parar: %d · outras respostas: %d' % (
             sum(1 for v in tudo if v.get('resultado') == 'saiu'),
             sum(1 for v in tudo if v.get('resultado') == 'trabalhando'),
             sum(1 for v in tudo if v.get('resultado') == 'parar'),
             sum(1 for v in tudo if not v.get('resultado') and v.get('resposta_vista')))]
    if saiu:
        L.append('\nViraram quentíssimo hoje:')
        L += ['• %s, com %s' % (v['nome'] or 'Sem nome', v.get('vendedora') or 'o time') for v in saiu]
    rev = [v for v in tudo if v.get('revisita') and v['enviado'].startswith(hoje)]
    if rev:
        L.append('Revisitas de hoje (disseram que estavam em dia, há 60 dias ou mais): %d' % len(rev))
    zapi(RESUMO_TEL, '\n'.join(L))
    print('\n'.join(L))


def mostrar_fila(n):
    estado = carregar()
    con = sqlite3.connect('file:%s?mode=ro' % DB, uri=True, timeout=20)
    f = fila(con, estado)
    con.close()
    print('FILA: %d pessoas, do contato mais antigo para o mais novo' % len(f))
    print('ritmo: %d por dia -> cerca de %d dias uteis' % (TETO_DIA, -(-len(f) // TETO_DIA)))
    for i, x in enumerate(f[:n], 1):
        print('  %2d. #%-5d desde %s  %-15s %-8s %s%s' % (i, x['id'], str(x['criado'])[:10], x['sit'], x['temp'],
                                                       (x['nome'] or '')[:28], '  REVISITA' if x['revisita'] else ''))


def teste(fone):
    estado = carregar()
    con = sqlite3.connect('file:%s?mode=ro' % DB, uri=True, timeout=20)
    zapi(fone, '*TESTE do fluxo "a dívida já venceu?"*\nAs próximas mensagens são o que os 3 primeiros da fila '
               'receberiam. Nada foi enviado para eles.')
    for lead in fila(con, estado)[:3]:
        ctx = MP.contexto(con, lead['id'])
        msg, prob = MP.escrever(ctx)
        time.sleep(MIN_ENTRE_ENVIOS)
        zapi(fone, '👤 *Para %s* (falou com a gente em %s)\n\n%s%s'
             % (lead['nome'] or 'sem nome', str(lead['criado'])[:10], msg,
                ('\n\n⚠️ conferência: ' + prob) if prob else ''))
        print('teste enviado: #%d %s %s' % (lead['id'], lead['nome'], prob or 'OK'))
    con.close()


if __name__ == '__main__':
    a = sys.argv
    if '--fila' in a:
        mostrar_fila(int(a[a.index('--fila') + 1]))
    elif '--enviar' in a:
        enviar_proximo()
    elif '--varrer' in a:
        varrer()
    elif '--resumo' in a:
        resumo()
    elif '--teste' in a:
        teste(a[a.index('--teste') + 1])
