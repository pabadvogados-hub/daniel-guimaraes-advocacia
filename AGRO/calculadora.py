"""
CALCULADORA DO CREDITO RURAL (juros + prorrogacao) - Daniel Guimaraes Advocacia.

Duas saidas, ambas HTML autocontido (sem internet, abre no celular):

1) PAGINA INTERATIVA (para o site ou para mandar como arquivo/link ao lead):
     saida/calculadora/index.html
   O proprio produtor digita os dados e ve parcela, juros, custo efetivo e o efeito de uma
   prorrogacao. E gerada a partir de modelos/calculadora_pagina.html com os dados e as cores de
   config_comercial.py.

2) SIMULACAO PRONTA DE UM LEAD (quando a equipe ja tem os numeros da cedula):
     saida/calculadora/simulacao_<lead>_<data>.html  (relatorio para enviar ao lead)
     saida/calculadora/simulacao_<lead>_<data>.txt   (resumo em texto para colar no WhatsApp)
   Mostra o cronograma atual e, se pedido, o cenario com prazo prorrogado (mesma taxa).

PNG: a ferramenta original nao gera imagem; aqui tambem nao. Para imagem/PDF, abra o HTML no
navegador e use "Imprimir ou salvar em PDF" (ou um print de tela).

Provimento 205/2021 da OAB: nao promete resultado, nao mostra honorario, nao coleta dado
(a pagina so abre o WhatsApp se a pessoa clicar).
"""
import json
import os
import re
import unicodedata
from datetime import datetime

from config_comercial import (ESCRITORIO, MENSAGEM_WHATSAPP_CALCULADORA, WHATSAPP_CALCULADORA, CORES,
                              preenchido)
from html_util import cartoes, esc, lista, numero, pagina, reais, tabela

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(AQUI, 'modelos', 'calculadora_pagina.html')
SAIDA_PADRAO = os.path.join(AQUI, 'saida', 'calculadora')
BLOCO = re.compile(r'<!-- CONFIG-INICIO -->.*?<!-- CONFIG-FIM -->', re.S)

PERIODOS = {'anual': 1, 'semestral': 2, 'mensal': 12}
NOME_PERIODO = {1: 'anual', 2: 'semestral', 12: 'mensal'}


class ErroCalculadora(ValueError):
    pass


# ============================================================
# CALCULO (mesma matematica da pagina interativa)
# ============================================================

def taxa_mensal(taxa, tipo):
    t = taxa / 100.0
    return t if tipo == 'am' else (1 + t) ** (1 / 12) - 1


def simular(p):
    """
    p: dict com valor, taxa, tipo ('aa'|'am'), parcelas, por_ano (1|2|12), sistema ('price'|'sac'),
       carencia (meses), carencia_juros ('pagos'|'capitalizados').
    Linha do tempo mensal: mes 0 = liberacao (ou data-base do saldo).
    """
    im = taxa_mensal(p['taxa'], p['tipo'])
    mpp = 12 // p['por_ano']                      # meses por parcela
    ip = (1 + im) ** mpp - 1                      # taxa do periodo da parcela
    saldo = p['valor']
    linhas, fluxo = [], []

    if p['carencia'] > 0:
        if p['carencia_juros'] == 'capitalizados':
            cresc = p['valor'] * ((1 + im) ** p['carencia'] - 1)
            saldo += cresc
            linhas.append({'rot': 'Carência', 'mes': p['carencia'], 'juros': cresc, 'amort': 0.0, 'pag': 0.0,
                           'saldo': saldo, 'carencia': True})
        else:
            mes = 0
            while mes < p['carencia']:
                passo = min(mpp, p['carencia'] - mes)
                mes += passo
                j = saldo * ((1 + im) ** passo - 1)
                linhas.append({'rot': 'Carência', 'mes': mes, 'juros': j, 'amort': 0.0, 'pag': j,
                               'saldo': saldo, 'carencia': True})
                fluxo.append((mes, j))

    base, n = saldo, p['parcelas']
    pmt = base / n if ip == 0 else base * ip / (1 - (1 + ip) ** -n)
    amort_sac = base / n
    primeira = ultima = 0.0
    for k in range(1, n + 1):
        jk = saldo * ip
        if p['sistema'] == 'price':
            pk = pmt
            ak = pk - jk
        else:
            ak = amort_sac
            pk = ak + jk
        if k == n:
            ak = saldo
            pk = ak + jk
        saldo = max(0.0, saldo - ak)
        m = p['carencia'] + k * mpp
        linhas.append({'rot': str(k), 'mes': m, 'juros': jk, 'amort': ak, 'pag': pk, 'saldo': saldo,
                       'carencia': False})
        fluxo.append((m, pk))
        if k == 1:
            primeira = pk
        ultima = pk

    total_pago = sum(v for _, v in fluxo)
    return {'linhas': linhas, 'fluxo': fluxo, 'juros_total': total_pago - p['valor'], 'total_pago': total_pago,
            'primeira': primeira, 'ultima': ultima, 'taxa_ano': (1 + im) ** 12 - 1}


def custo_efetivo_anual(liquido, fluxo):
    """Taxa que iguala o valor liquido recebido aos pagamentos (TIR mensal anualizada). None se nao converge."""
    if liquido <= 0:
        return None

    def vp(i):
        return sum(v / (1 + i) ** mes for mes, v in fluxo) - liquido

    lo, hi = -0.99, 1.0
    try:
        if vp(lo) * vp(hi) > 0:
            return None
    except OverflowError:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if vp(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (1 + (lo + hi) / 2) ** 12 - 1


def validar(p):
    if not p['valor'] > 0:
        return 'Informe o valor financiado ou o saldo devedor (--valor).'
    if p['taxa'] is None or p['taxa'] < 0:
        return 'Informe a taxa de juros (--taxa).'
    if p['tipo'] == 'am' and p['taxa'] > 20:
        return 'Confira a taxa: mais de 20% ao mês parece fora do normal.'
    if p['tipo'] == 'aa' and p['taxa'] > 300:
        return 'Confira a taxa: parece alta demais para % ao ano.'
    if not 1 <= p['parcelas'] <= 600:
        return 'Informe o número de parcelas (de 1 a 600).'
    if not 0 <= p['carencia'] <= 120:
        return 'Carência entre 0 e 120 meses.'
    if p.get('custos', 0) < 0 or p.get('custos', 0) >= p['valor']:
        return 'Os custos iniciais precisam ser menores que o valor financiado.'
    if not 0 <= p.get('prorrogar_anos', 0) <= 30:
        return 'Prorrogação entre 0 e 30 anos.'
    return ''


def valor_br(txt):
    """Aceita 500000 | 500000.50 | 500.000,50 | R$ 500.000,50."""
    if txt is None:
        return None
    if isinstance(txt, (int, float)):
        return float(txt)
    t = re.sub(r'\s|R\$', '', str(txt))
    if not t:
        return None
    if ',' in t:
        t = t.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(\.\d{3})+', t):
        t = t.replace('.', '')
    try:
        return float(t)
    except ValueError:
        raise ErroCalculadora(f'Valor inválido: {txt!r}')


# ============================================================
# PAGINA INTERATIVA
# ============================================================

def _numero_whatsapp(numero_cli=None):
    bruto = numero_cli if numero_cli is not None else WHATSAPP_CALCULADORA
    if not preenchido(bruto):
        return ''
    d = re.sub(r'\D', '', bruto)
    if len(d) in (10, 11):
        d = '55' + d
    if len(d) not in (12, 13):
        raise ErroCalculadora(f'Número de WhatsApp inválido: {bruto!r} (use DDI+DDD+número, ex.: 5500000000000)')
    return d


def _campo(nome):
    v = ESCRITORIO.get(nome, '')
    return v if preenchido(v) else ''


def gerar_pagina(whatsapp=None, saida=None):
    if not os.path.exists(MODELO):
        raise ErroCalculadora(f'Modelo da página não encontrado: {MODELO}')
    pasta = saida or SAIDA_PADRAO
    os.makedirs(pasta, exist_ok=True)
    responsavel = _campo('responsavel')
    if responsavel and _campo('oab'):
        responsavel += ' - ' + _campo('oab')
    endereco = _campo('endereco')
    if _campo('cidade_uf') and _campo('cidade_uf') not in endereco:
        endereco = ', '.join(x for x in (endereco, _campo('cidade_uf')) if x)
    config = {
        'whatsapp': _numero_whatsapp(whatsapp),
        'mensagem': MENSAGEM_WHATSAPP_CALCULADORA,
        'escritorio': ESCRITORIO['nome'],
        'responsavel': responsavel,
        'endereco': endereco,
        'site': _campo('site'),
        'instagram': _campo('instagram'),
    }
    corpo = ',\n'.join(f'  {k}: {json.dumps(v, ensure_ascii=False)}' for k, v in config.items())
    c = CORES
    cores = (':root{\n'
             f"  --marinho:{c['marinho']}; --marinho-claro:{c['marinho_claro']}; --oliva:{c['oliva']}; "
             f"--oliva-escuro:{c['oliva_escuro']}; --oliva-claro:{c['oliva_claro']};\n"
             f"  --texto:{c['texto']}; --suave:{c['suave']}; --linha:{c['linha']}; --fundo:#FFFFFF; "
             f"--papel:{c['papel']};\n"
             f"  --verde:{c['whatsapp']}; --verde-escuro:{c['whatsapp_escuro']};\n}}")
    bloco = ('<!-- CONFIG-INICIO -->\n<script>\nwindow.CONFIG_CALCULADORA = {\n' + corpo +
             '\n};\n</script>\n<style>\n' + cores + '\n</style>\n<!-- CONFIG-FIM -->')
    with open(MODELO, encoding='utf-8') as f:
        html_modelo = f.read()
    if not BLOCO.search(html_modelo):
        raise ErroCalculadora('Bloco CONFIG-INICIO/CONFIG-FIM não encontrado no modelo da página')
    html_final = BLOCO.sub(lambda _: bloco, html_modelo, count=1)
    destino = os.path.join(pasta, 'index.html')
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(html_final)
    print('Página interativa da calculadora:')
    print(f'  {destino}')
    if config['whatsapp']:
        print(f"  WhatsApp do botão: +{config['whatsapp']}")
    else:
        print('  Botão do WhatsApp DESLIGADO (WHATSAPP_CALCULADORA = [PREENCHER] em config_comercial.py '
              'ou use --whatsapp 55DDDNUMERO).')
    return destino


# ============================================================
# SIMULACAO PRONTA PARA UM LEAD
# ============================================================

def _slug(txt):
    t = unicodedata.normalize('NFKD', txt or '').encode('ascii', 'ignore').decode()
    t = re.sub(r'[^A-Za-z0-9]+', '_', t).strip('_')
    return (t or 'lead')[:40]


def _pct(v):
    return '-' if v is None else numero(100 * v, 2) + '%'


def _tabela_cronograma(r):
    L = r['linhas']
    mostrar = L if len(L) <= 30 else L[:18] + [None] + L[-3:]
    linhas = []
    for l in mostrar:
        if l is None:
            linhas.append([f'... {len(L) - 21} parcelas omitidas ...', '', '', '', '', ''])
            continue
        linhas.append(['Carência' if l['carencia'] else f"Parcela {l['rot']}", (str(l['mes']), l['mes']),
                       (reais(l['juros']), round(l['juros'], 2)), (reais(l['amort']), round(l['amort'], 2)),
                       (reais(l['pag']), round(l['pag'], 2)), (reais(l['saldo']), round(l['saldo'], 2))])
    linhas.append(['Total', '', (reais(sum(l['juros'] for l in L)), 0), (reais(sum(l['amort'] for l in L)), 0),
                   (reais(r['total_pago']), 0), ''])
    return tabela(['Parcela', 'Mês', 'Juros', 'Amortização', 'Pagamento', 'Saldo devedor'], linhas,
                  ordenavel=False)


def gerar_simulacao(p, lead='', banco='', saida=None):
    """Gera o relatorio HTML + resumo TXT de uma simulacao. Devolve (html, txt, resultado)."""
    erro = validar(p)
    if erro:
        raise ErroCalculadora(erro)
    pasta = saida or SAIDA_PADRAO
    os.makedirs(pasta, exist_ok=True)

    r = simular(p)
    cet = custo_efetivo_anual(p['valor'] - p.get('custos', 0), r['fluxo'])
    periodo = NOME_PERIODO[p['por_ano']]
    periodos = periodo[:-1] + 'is'          # anual -> anuais, mensal -> mensais
    un = '% ao mês' if p['tipo'] == 'am' else '% ao ano'
    parcela_txt = reais(r['primeira']) if p['sistema'] == 'price' else f"{reais(r['primeira'])} a {reais(r['ultima'])}"

    rp = None
    anos = p.get('prorrogar_anos', 0) or 0
    if anos:
        pp = dict(p, parcelas=p['parcelas'] + anos * p['por_ano'],
                  carencia=p['carencia'] + (p.get('prorrogar_carencia', 0) or 0))
        rp = simular(pp)
        rp['parcelas'] = pp['parcelas']
        rp['carencia'] = pp['carencia']

    rc = None
    if p.get('taxa_comparacao') is not None:
        rc = simular(dict(p, taxa=p['taxa_comparacao']))

    # ---------- HTML ----------
    dados = [
        f"Valor considerado (financiado ou saldo devedor): {reais(p['valor'])}",
        f"Taxa: {numero(p['taxa'], 2)}{un} ({p['sistema'].upper()}, {p['parcelas']} parcelas {periodos})",
        f"Carência: {p['carencia']} meses" + (f" (juros {p['carencia_juros']})" if p['carencia'] else ''),
    ]
    if banco:
        dados.append(f'Instituição: {banco}')
    if p.get('custos'):
        dados.append(f"Custos na liberação (tarifas, seguros, IOF): {reais(p['custos'])}")

    blocos = [
        ('Dados usados na simulação', lista(dados)),
        ('Resultado do contrato como está', cartoes([
            (parcela_txt, f'parcela {periodo}' + (' (1ª à última)' if p['sistema'] == 'sac' else '')),
            (reais(r['juros_total']), 'total de juros'),
            (reais(r['total_pago']), 'total pago'),
            (_pct(r['juros_total'] / p['valor']), 'juros sobre o valor'),
            (_pct(r['taxa_ano']), 'taxa efetiva ao ano'),
            (_pct(cet), 'custo efetivo anual (com custos)'),
        ])),
    ]
    if rp:
        reducao = 1 - rp['primeira'] / r['primeira'] if r['primeira'] else 0
        comp = tabela(['', 'Como está', f'Com prorrogação (+{anos} ano{"s" if anos > 1 else ""})'], [
            ['Parcelas', f"{p['parcelas']} {periodos}", f"{rp['parcelas']} {periodos}"],
            ['Carência (meses)', str(p['carencia']), str(rp['carencia'])],
            ['1ª parcela', (reais(r['primeira']), 0), (reais(rp['primeira']), 0)],
            ['Total de juros', (reais(r['juros_total']), 0), (reais(rp['juros_total']), 0)],
            ['Total pago', (reais(r['total_pago']), 0), (reais(rp['total_pago']), 0)],
        ], ordenavel=False)
        blocos.append(('Cenário com prazo prorrogado (mesma taxa)', comp + (
            f'<p class="nota">Com o prazo maior, a 1ª parcela fica {_pct(reducao)} menor. O total de juros '
            'sobe porque o dinheiro fica mais tempo emprestado. Comparação apenas matemática: não indica '
            'que o banco vai concordar nem o resultado de pedido algum.</p>')))
    if rc:
        dif = r['juros_total'] - rc['juros_total']
        blocos.append(('Comparação com outra taxa', (
            f'<p>Com a taxa de <b>{numero(p["taxa_comparacao"], 2)}{un}</b>, o total de juros seria '
            f'<b>{reais(rc["juros_total"])}</b> - diferença de <b>{reais(abs(dif))}</b> '
            f'{"a menos" if dif >= 0 else "a mais"} que na taxa da cédula. Comparação apenas matemática.</p>')))
    blocos += [
        ('Cronograma (taxa da cédula)', _tabela_cronograma(r)),
        ('Prorrogação da dívida rural: o que diz a regra', (
            '<p>O Manual de Crédito Rural do Banco Central (MCR, Capítulo 2, Seção 6, item 4) prevê a prorrogação '
            'da dívida rural, mantidos os encargos do contrato, quando o produtor comprova dificuldade temporária de '
            'pagamento causada, por exemplo, por dificuldade de comercialização, frustração de safra por fatores '
            'adversos (seca, excesso de chuva, pragas) ou outras ocorrências prejudiciais à atividade.</p>'
            '<p>A Súmula 298 do Superior Tribunal de Justiça diz que o alongamento de dívida originada de crédito '
            'rural não é faculdade da instituição financeira, mas direito do devedor nos termos da lei.</p>')),
        ('Documentos que ajudam a analisar o caso', lista([
            'Cédulas de crédito rural e aditivos', 'Extratos e comprovantes de pagamento',
            'Notificações, cobranças ou citação do banco (execução, leilão, busca e apreensão)',
            'Registro da perda: laudo técnico, fotos, notas fiscais de venda, dados de produtividade',
        ])),
        (None, '<div class="aviso"><b>Aviso:</b> simulação apenas informativa. Os valores são aproximados e não '
               'substituem a leitura do contrato: capitalização, IOF, seguros, tarifas, correção e encargos de '
               'atraso podem alterar o resultado. A taxa anual é tratada como taxa efetiva (juros compostos). '
               'Não é consultoria financeira e não representa promessa de resultado.</div>'),
    ]
    titulo = 'Simulação do crédito rural'
    sub = (f'Preparada para {lead}' if lead else 'Simulação informativa') + f" - {ESCRITORIO['nome']}"
    agora = datetime.now()
    base = os.path.join(pasta, f"simulacao_{_slug(lead)}_{agora.strftime('%Y%m%d_%H%M%S')}")
    with open(base + '.html', 'w', encoding='utf-8') as f:
        f.write(pagina(titulo, sub, blocos, 'Valores aproximados; não é promessa de resultado.'))

    # ---------- TXT (para colar no WhatsApp) ----------
    txt = [f'Simulação do seu crédito rural{" - " + lead if lead else ""}', '',
           f"Valor considerado: {reais(p['valor'])}",
           f"Taxa: {numero(p['taxa'], 2)}{un} | {p['parcelas']} parcelas {periodos} ({p['sistema'].upper()})"
           + (f" | carência {p['carencia']} meses" if p['carencia'] else ''),
           f'Parcela {periodo}: {parcela_txt}',
           f"Total de juros: {reais(r['juros_total'])}",
           f"Total pago: {reais(r['total_pago'])}"]
    if rp:
        txt += ['', f"Com {anos} ano(s) a mais de prazo (mesma taxa): 1ª parcela de {reais(rp['primeira'])} "
                    f"e total de juros de {reais(rp['juros_total'])}."]
    txt += ['', 'Simulação informativa, valores aproximados; não substitui a análise do contrato '
                'e não é promessa de resultado.', ESCRITORIO['nome']]
    with open(base + '.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt) + '\n')

    print('Simulação gerada:')
    print(f'  {base}.html  (relatório para enviar ao lead)')
    print(f'  {base}.txt   (resumo para colar no WhatsApp)')
    print(f'  Parcela {periodo}: {parcela_txt} | juros {reais(r["juros_total"])} | total {reais(r["total_pago"])}')
    if rp:
        print(f'  Com +{anos} ano(s): 1a parcela {reais(rp["primeira"])} | juros {reais(rp["juros_total"])}')
    print('  PNG: não gerado (a ferramenta não depende de navegador). Para imagem ou PDF, abra o HTML e use '
          'Imprimir > Salvar como PDF, ou um print de tela.')
    return base + '.html', base + '.txt', r


def params_de_args(a):
    """Converte os argumentos da CLI no dict de simular()."""
    return {
        'valor': valor_br(a.valor),
        'taxa': valor_br(a.taxa),
        'tipo': 'am' if a.taxa_tipo == 'am' else 'aa',
        'parcelas': a.parcelas,
        'por_ano': PERIODOS[a.periodicidade],
        'sistema': a.sistema,
        'carencia': a.carencia,
        'carencia_juros': a.carencia_juros,
        'custos': valor_br(a.custos) or 0.0,
        'taxa_comparacao': valor_br(a.taxa_comparacao),
        'prorrogar_anos': a.prorrogar_anos or 0,
        'prorrogar_carencia': a.prorrogar_carencia or 0,
    }
