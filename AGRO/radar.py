"""
RADAR DO CREDITO RURAL POR MUNICIPIO (dados publicos do Banco Central/SICOR + IBGE).

Termometro para decidir ONDE anunciar e prospectar: municipios e regioes com mais produtores
tomando credito rural (quantidade de contratos), mais volume financiado e mais custeio nos
produtos de foco (config_comercial.RADAR['produtos_foco']).

Saidas em saida/radar/ (ou --saida): CSV (abre no Excel), HTML com tabela ordenavel e JSON.

Limites (dizer sempre a quem decide):
- SICOR mostra contratos NOVOS emitidos no ano, nao saldo devedor nem inadimplencia por municipio.
- E dado agregado e anonimo: nao ha nome, CPF ou contrato de ninguem (sigilo bancario).
  O radar serve para segmentar anuncio institucional por regiao, nunca para abordar pessoas.
"""
import csv
import json
import os
import unicodedata
from bisect import bisect_right
from collections import defaultdict
from datetime import date

import sicor
from config_comercial import RADAR
from html_util import cartoes, esc, lista, numero, pagina, reais, reais_curto, tabela

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA_PADRAO = os.path.join(AQUI, 'saida', 'radar')


def _float(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def _norm(txt):
    t = unicodedata.normalize('NFKD', txt or '').encode('ascii', 'ignore').decode()
    return ' '.join(t.lower().replace('-', ' ').replace("'", ' ').split())


def _campo_produto(produto):
    return 'vl_' + _norm(produto).replace(' ', '_')


def _progresso(rotulo):
    def aviso(n):
        print(f'\r   {rotulo}: {n} linhas', end='', flush=True)
    return aviso


def coletar_uf(uf, ano, produtos, cache=None):
    """Consolida um estado: ({codigo_ibge: registro do municipio}, [avisos de meses que falharam])."""
    uf = uf.upper()
    faltas = []
    print(f'\n[{uf} {ano}] municipios (IBGE)...', flush=True)
    try:
        nomes = sicor.municipios_ibge(uf)
    except Exception as e:  # nome oficial e so enfeite: segue com o nome do SICOR
        print(f'   aviso: IBGE indisponivel ({type(e).__name__}); usando nomes do SICOR')
        nomes = {}

    def novo():
        reg = {'uf': uf, 'codigo_ibge': '', 'municipio': '', 'mesorregiao': '',
               'qtd_custeio': 0, 'vl_custeio': 0.0, 'qtd_invest': 0, 'vl_invest': 0.0,
               'vl_agricola': 0.0, 'vl_pecuaria': 0.0, 'area_custeio_ha': 0.0}
        for p in produtos:
            reg[_campo_produto(p)] = 0.0
        return reg

    mun = defaultdict(novo)

    linhas, falharam = sicor.totais_municipio(uf, ano, aviso=_progresso('custeio + investimento'), cache=cache)
    print()
    if falharam:
        faltas.append(f"{uf} contratos (custeio + investimento): meses {', '.join(map(str, falharam))} nao baixados")
    for r in linhas:
        cod = str(r.get('codMunicIbge') or '').strip()
        if not cod:
            continue
        m = mun[cod]
        m['codigo_ibge'] = cod
        m['municipio'] = m['municipio'] or (r.get('Municipio') or '').strip()
        qc, vc = int(r.get('QtdCusteio') or 0), _float(r.get('VlCusteio'))
        qi, vi = int(r.get('QtdInvestimento') or 0), _float(r.get('VlInvestimento'))
        m['qtd_custeio'] += qc
        m['vl_custeio'] += vc
        m['qtd_invest'] += qi
        m['vl_invest'] += vi
        m['area_custeio_ha'] += _float(r.get('AreaCusteio'))
        if r.get('Atividade') == '1':
            m['vl_agricola'] += vc + vi
        elif r.get('Atividade') == '2':
            m['vl_pecuaria'] += vc + vi

    for produto in produtos:
        campo = _campo_produto(produto)
        linhas, falharam = sicor.custeio_por_produto(uf, ano, produto,
                                                     aviso=_progresso(f'custeio {produto.lower()}'), cache=cache)
        print()
        if falharam:
            faltas.append(f"{uf} custeio {produto.lower()}: meses {', '.join(map(str, falharam))} nao baixados")
        for r in linhas:
            cod = str(r.get('codIbge') or '').strip()
            if not cod:
                continue
            m = mun[cod]
            m['codigo_ibge'] = cod
            m['municipio'] = m['municipio'] or (r.get('Municipio') or '').strip()
            m[campo] += _float(r.get('VlCusteio'))

    for cod, m in mun.items():
        if cod in nomes:
            m['municipio'] = nomes[cod]['nome']
            m['mesorregiao'] = nomes[cod]['mesorregiao']
    return dict(mun), faltas


def completar(registros, produtos):
    for m in registros:
        m['qtd_total'] = m['qtd_custeio'] + m['qtd_invest']
        m['vl_total'] = m['vl_custeio'] + m['vl_invest']
        m['vl_medio_contrato'] = m['vl_total'] / m['qtd_total'] if m['qtd_total'] else 0.0
        m['vl_foco'] = sum(m.get(_campo_produto(p), 0.0) for p in produtos)
    return registros


def _percentis(valores):
    ordenados = sorted(valores)
    n = len(ordenados)
    return lambda v: 100.0 * bisect_right(ordenados, v) / n if n else 0.0


def pontuar(registros):
    """Indice de prioridade 0-100: percentil de contratos, de valor e dos produtos de foco (pesos em config)."""
    if not registros:
        return registros
    p_qtd = _percentis([r['qtd_total'] for r in registros])
    p_vl = _percentis([r['vl_total'] for r in registros])
    p_foco = _percentis([r['vl_foco'] for r in registros])
    for r in registros:
        r['indice'] = round(RADAR['peso_contratos'] * p_qtd(r['qtd_total'])
                            + RADAR['peso_valor'] * p_vl(r['vl_total'])
                            + RADAR['peso_foco'] * p_foco(r['vl_foco']), 1)
    registros.sort(key=lambda r: (r['indice'], r['vl_total']), reverse=True)
    for i, r in enumerate(registros, 1):
        r['posicao'] = i
    return registros


def por_regiao(registros):
    """Ranking de mesorregioes (UF + mesorregiao do IBGE) por valor financiado."""
    grupos = defaultdict(lambda: {'municipios': 0, 'qtd_total': 0, 'vl_total': 0.0, 'vl_foco': 0.0})
    for r in registros:
        g = grupos[(r['uf'], r['mesorregiao'] or '(sem mesorregião)')]
        g['municipios'] += 1
        g['qtd_total'] += r['qtd_total']
        g['vl_total'] += r['vl_total']
        g['vl_foco'] += r['vl_foco']
    saida = [dict(uf=uf, regiao=reg, **v) for (uf, reg), v in grupos.items()]
    saida.sort(key=lambda g: g['vl_total'], reverse=True)
    return saida


def sugerir(registros, produtos, quantos=None):
    """Municipios prioritarios para anuncio/prospeccao (maior indice com contratos no ano)."""
    quantos = quantos or RADAR['top_sugestao']
    saida = []
    for r in [r for r in registros if r['qtd_total'] > 0][:quantos]:
        partes = [f"{numero(r['qtd_total'])} contratos", f"{reais(r['vl_total'])} financiados"]
        for p in produtos:
            v = r.get(_campo_produto(p), 0.0)
            if v:
                partes.append(f'{p.lower()} {reais(v)}')
        partes.append(f"média {reais(r['vl_medio_contrato'])} por contrato")
        saida.append({'municipio': r['municipio'], 'uf': r['uf'], 'indice': r['indice'],
                      'motivo': '; '.join(partes)})
    return saida


def filtrar_municipios(registros, nomes):
    """Mantem so os municipios pedidos (comparacao sem acento/maiuscula). Devolve (filtrados, nao_achados)."""
    alvo = {_norm(n): n for n in nomes if n.strip()}
    achados = [r for r in registros if _norm(r['municipio']) in alvo]
    vistos = {_norm(r['municipio']) for r in achados}
    return achados, [n for k, n in alvo.items() if k not in vistos]


def colunas(produtos):
    base = [
        ('posicao', 'Posição'), ('uf', 'UF'), ('municipio', 'Município'), ('mesorregiao', 'Mesorregião'),
        ('indice', 'Índice'), ('qtd_total', 'Contratos'), ('vl_total', 'Valor total (R$)'),
        ('qtd_custeio', 'Contratos custeio'), ('vl_custeio', 'Custeio (R$)'),
        ('qtd_invest', 'Contratos investimento'), ('vl_invest', 'Investimento (R$)'),
        ('vl_medio_contrato', 'Média por contrato (R$)'), ('vl_agricola', 'Agrícola (R$)'),
        ('vl_pecuaria', 'Pecuária (R$)'),
    ]
    base += [(_campo_produto(p), f'Custeio {p.lower()} (R$)') for p in produtos]
    return base + [('codigo_ibge', 'Código IBGE')]


def salvar_csv(registros, produtos, caminho):
    cols = colunas(produtos)
    with open(caminho, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow([t for _, t in cols])
        for r in registros:
            linha = []
            for c, _ in cols:
                v = r.get(c, '')
                if isinstance(v, float):
                    v = f'{v:.2f}'.replace('.', ',')
                linha.append(v)
            w.writerow(linha)


def salvar_html(registros, regioes, sugestoes, produtos, rotulo, ano, caminho, faltas=None, ficticio=False):
    total_qtd = sum(r['qtd_total'] for r in registros)
    total_vl = sum(r['vl_total'] for r in registros)
    total_foco = sum(r['vl_foco'] for r in registros)
    top_sug = {(s['municipio'], s['uf']) for s in sugestoes}
    parcial = ' (ano em curso: dados parciais)' if int(ano) >= date.today().year else ''
    nomes_foco = ' + '.join(p.lower() for p in produtos) or 'produtos de foco'

    linhas, destaque = [], set()
    for i, r in enumerate(registros):
        if (r['municipio'], r['uf']) in top_sug:
            destaque.add(i)
        linha = [
            (str(r['posicao']), r['posicao']), r['uf'], r['municipio'], r['mesorregiao'],
            (numero(r['indice'], 1), r['indice']), (numero(r['qtd_total']), r['qtd_total']),
            (reais(r['vl_total']), round(r['vl_total'], 2)), (numero(r['qtd_custeio']), r['qtd_custeio']),
            (reais(r['vl_custeio']), round(r['vl_custeio'], 2)), (numero(r['qtd_invest']), r['qtd_invest']),
            (reais(r['vl_invest']), round(r['vl_invest'], 2)),
            (reais(r['vl_medio_contrato']), round(r['vl_medio_contrato'], 2)),
        ]
        linha += [(reais(r.get(_campo_produto(p), 0)), round(r.get(_campo_produto(p), 0), 2)) for p in produtos]
        linhas.append(linha)
    cab = ['Pos.', 'UF', 'Município', 'Mesorregião', 'Índice', 'Contratos', 'Valor total', 'Contr. custeio',
           'Custeio', 'Contr. invest.', 'Investimento', 'Média/contrato'] + [f'Custeio {p.lower()}' for p in produtos]

    reg_linhas = [[g['uf'], g['regiao'], (numero(g['municipios']), g['municipios']),
                   (numero(g['qtd_total']), g['qtd_total']), (reais(g['vl_total']), round(g['vl_total'], 2)),
                   (reais(g['vl_foco']), round(g['vl_foco'], 2))] for g in regioes]

    sug_html = '<ol class="lista">' + ''.join(
        f"<li><b>{esc(s['municipio'])}/{esc(s['uf'])}</b> - índice {numero(s['indice'], 1)} - {esc(s['motivo'])}</li>"
        for s in sugestoes) + '</ol>'
    pc, pv, pf = (int(RADAR['peso_contratos'] * 100), int(RADAR['peso_valor'] * 100), int(RADAR['peso_foco'] * 100))
    como_ler = lista([
        f'Índice (0 a 100) = {pc}% quantidade de contratos + {pv}% valor financiado + {pf}% custeio de {nomes_foco}, '
        'cada um comparado com os demais municípios da consulta (pesos em AGRO/config_comercial.py).',
        'Muitos contratos = muitos produtores com crédito rural = mais público para o anúncio.',
        'Média por contrato alta = dívidas maiores (produtor de porte médio/grande).',
        'Use a lista para segmentar os anúncios por cidade (raio) e compare o custo por lead de cada região '
        'antes de mudar orçamento.',
    ])
    limites = lista([
        'Fonte: SICOR/Banco Central (Matriz de Dados do Crédito Rural, API Olinda) + IBGE. Dado público e agregado.',
        'O SICOR mostra contratos novos do ano, não o saldo devedor nem a inadimplência por município.',
        'Não há nome, CPF ou contrato de ninguém: o radar orienta anúncio institucional por região, '
        'nunca abordagem individual (Provimento 205/2021 da OAB).',
    ])
    blocos = []
    if ficticio:
        blocos.append(('EXEMPLO COM DADOS FICTÍCIOS', lista([
            'Municípios e números inventados só para mostrar o formato do relatório. '
            'Para dados reais: python main.py radar --uf <UF>.'], 'alerta')))
    if faltas:
        blocos.append(('DADOS INCOMPLETOS - rodar de novo', lista(
            faltas + ['O servidor do Banco Central não respondeu nesses meses. Rode o mesmo comando de novo: '
                      'os meses já baixados ficam guardados e só os que faltam são buscados.'], 'alerta')))
    blocos += [
        (None, cartoes([(numero(total_qtd), 'contratos de crédito rural'), (reais_curto(total_vl), 'financiados'),
                        (reais_curto(total_foco), f'custeio de {nomes_foco}'),
                        (numero(len(registros)), 'municípios'), (numero(len(regioes)), 'regiões')])),
        ('Onde anunciar e prospectar (sugestão)', sug_html),
        ('Regiões (mesorregiões do IBGE)', tabela(['UF', 'Região', 'Municípios', 'Contratos', 'Valor total',
                                                   f'Custeio {nomes_foco}'], reg_linhas)),
        ('Como ler', como_ler),
        ('Todos os municípios (clique no título da coluna para ordenar)', tabela(cab, linhas, destaque)),
        ('Limites do dado', limites),
    ]
    titulo = 'Radar do Crédito Rural'
    sub = f'{rotulo} - contratos emitidos em {ano}{parcial}'
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(pagina(titulo, sub, blocos, 'Fonte: Banco Central (SICOR) e IBGE.'))


def _salvar_e_resumir(registros, produtos, rotulo, ano, base, faltas, ficticio=False, municipios=None):
    regioes = por_regiao(registros)
    sugestoes = sugerir(registros, produtos)
    nao_achados = []
    exibidos = registros
    if municipios:
        exibidos, nao_achados = filtrar_municipios(registros, municipios)
        sugestoes = sugerir(exibidos, produtos)
    salvar_csv(exibidos, produtos, base + '.csv')
    salvar_html(exibidos, regioes, sugestoes, produtos, rotulo, ano, base + '.html', faltas, ficticio)
    with open(base + '.json', 'w', encoding='utf-8') as f:
        json.dump({'escopo': rotulo, 'ano': ano, 'ficticio': ficticio, 'incompleto': faltas,
                   'produtos_foco': produtos, 'sugestoes': sugestoes, 'regioes': regioes,
                   'municipios': exibidos}, f, ensure_ascii=False, indent=1)

    print(f'\n=== RADAR {rotulo} {ano}{" (FICTICIO)" if ficticio else ""} ===')
    if faltas:
        print('ATENCAO - DADOS INCOMPLETOS (o servidor do Banco Central falhou; rode de novo para completar):')
        for x in faltas:
            print(f'  - {x}')
    if nao_achados:
        print(f"Municipio(s) nao encontrado(s) nos dados: {', '.join(nao_achados)} (confira a grafia e a UF)")
    print(f'{len(registros)} municipios | {numero(sum(r["qtd_total"] for r in registros))} contratos | '
          f'{reais(sum(r["vl_total"] for r in registros))}')
    print('\nTop 5 regioes (valor financiado):')
    for g in regioes[:5]:
        print(f"  - {g['regiao']}/{g['uf']}: {numero(g['qtd_total'])} contratos, {reais(g['vl_total'])}")
    print('\nTop 10 municipios' + (' pedidos' if municipios else '') + ' (indice):')
    for r in exibidos[:10]:
        print(f"  {r['posicao']:>3}. {r['municipio']}/{r['uf']:<3} indice {r['indice']:>5}  "
              f"{numero(r['qtd_total']):>6} contratos  {reais(r['vl_total']):>20}")
    print(f'\nArquivos:\n  {base}.csv\n  {base}.html\n  {base}.json')
    return base


def gerar(ufs, ano=None, saida=None, municipios=None, produtos=None):
    """Radar real (rede). Levanta sicor.SemConexao / sicor.ErroSicor em falha de rede."""
    ufs = [u.strip().upper() for u in ufs if u.strip()]
    produtos = [p.strip().upper() for p in (produtos if produtos is not None else RADAR['produtos_foco'])
                if p.strip()]
    ano = int(ano or date.today().year - 1)
    pasta = saida or SAIDA_PADRAO
    os.makedirs(pasta, exist_ok=True)

    print('Testando acesso a API Olinda do Banco Central...', flush=True)
    sicor.testar_conexao()

    cache = os.path.join(pasta, 'cache')
    registros, faltas = [], []
    for uf in ufs:
        dados_uf, faltas_uf = coletar_uf(uf, ano, produtos, cache)
        registros += list(dados_uf.values())
        faltas += faltas_uf
    registros = pontuar([r for r in completar(registros, produtos) if r['qtd_total'] or r['vl_foco']])
    if not registros:
        raise sicor.ErroSicor('nenhum dado retornado pela API para ' + ', '.join(ufs) + f' em {ano}'
                              + (' (' + '; '.join(faltas) + ')' if faltas else ''))

    rotulo = 'Brasil' if len(ufs) == len(sicor.UFS_DISPONIVEIS) else ', '.join(ufs)
    nome = 'BRASIL' if rotulo == 'Brasil' else '-'.join(ufs)
    base = os.path.join(pasta, f"radar_{nome}_{ano}" + ('_INCOMPLETO' if faltas else ''))
    return _salvar_e_resumir(registros, produtos, rotulo, ano, base, faltas, municipios=municipios)


def gerar_exemplo(arquivo_json, saida=None):
    """Radar com dados FICTICIOS (sem rede), so para mostrar o formato do relatorio."""
    with open(arquivo_json, encoding='utf-8') as f:
        dados = json.load(f)
    produtos = dados['produtos_foco']
    registros = pontuar(completar(dados['municipios'], produtos))
    pasta = saida or SAIDA_PADRAO
    os.makedirs(pasta, exist_ok=True)
    base = os.path.join(pasta, f"radar_EXEMPLO_FICTICIO_{dados['ano']}")
    return _salvar_e_resumir(registros, produtos, dados['escopo'], dados['ano'], base, [], ficticio=True)
