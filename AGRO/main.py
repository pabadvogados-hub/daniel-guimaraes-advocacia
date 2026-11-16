"""
FERRAMENTAS AGRO - Daniel Guimaraes Advocacia (defesa do produtor rural contra bancos)

  Calculadora do credito rural (juros + prorrogacao):
    python main.py calculadora                                  (so a pagina interativa)
    python main.py calculadora --valor 850000 --taxa 12,5 --parcelas 5 --prorrogar-anos 3 --lead "Nome"
                                                                (simulacao pronta para mandar ao lead)

  Radar do credito rural (SICOR/Banco Central, dados publicos):
    python main.py radar --uf GO                                (uma UF, ano anterior)
    python main.py radar --uf GO,MT --ano 2025 --municipio "Rio Verde,Jatai"
    python main.py radar --uf TODAS                             (Brasil inteiro: demora bastante)

  Exemplo completo com dados ficticios (funciona sem internet):
    python main.py exemplo

Roda de qualquer pasta: python AGRO/main.py ... ou cd AGRO && python main.py ...
Saidas em AGRO/saida/. Configuracao em AGRO/config_comercial.py.
"""
import argparse
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
EXEMPLOS = os.path.join(AQUI, 'exemplos')
SAIDA = os.path.join(AQUI, 'saida')

# console do Windows (cp1252): nunca quebrar o print por causa de um caractere
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass


def _erro(msg, codigo=1):
    print(f'ERRO: {msg}', file=sys.stderr)
    return codigo


def _msg_rede(e):
    import sicor
    msg = f'Nao foi possivel acessar a API Olinda do Banco Central: {e}. '
    if isinstance(e, sicor.SemConexao):
        return msg + 'Verifique a conexao e tente de novo.'
    return msg + ('Verifique a conexao. Se a internet estiver ok, o servidor do Banco Central esta '
                  'devolvendo erro (ele oscila bastante): tente de novo mais tarde; os meses ja baixados '
                  'ficam em cache.')


def cmd_calculadora(a):
    import calculadora
    try:
        calculadora.gerar_pagina(a.whatsapp, a.saida)
        if a.valor is None:
            print('\nPara gerar a simulacao de um lead, informe ao menos --valor, --taxa e --parcelas '
                  '(veja: python main.py calculadora --help).')
            return 0
        if a.taxa is None or a.parcelas is None:
            return _erro('para a simulacao informe tambem --taxa e --parcelas.')
        print()
        calculadora.gerar_simulacao(calculadora.params_de_args(a), a.lead or '', a.banco or '', a.saida)
    except calculadora.ErroCalculadora as e:
        return _erro(str(e))
    return 0


def cmd_radar(a):
    import radar
    import sicor
    bruto = a.uf.replace(' ', ',').upper()
    if bruto in ('TODAS', 'BR', 'BRASIL'):
        ufs = list(sicor.UFS_DISPONIVEIS)
    else:
        ufs = [u for u in bruto.split(',') if u]
    invalidas = [u for u in ufs if u not in sicor.UF_SICOR]
    if not ufs or invalidas:
        return _erro(f"UF invalida: {', '.join(invalidas) or '(vazia)'}. "
                     f"Disponiveis: {', '.join(sicor.UFS_DISPONIVEIS)} ou TODAS.")
    municipios = [m.strip() for m in (a.municipio or '').split(',') if m.strip()]
    produtos = None if a.produtos is None else [p for p in a.produtos.split(',') if p.strip()]
    sicor.configurar(a.timeout, a.tentativas)
    try:
        radar.gerar(ufs, a.ano, a.saida, municipios, produtos)
    except sicor.ErroSicor as e:
        print()
        return _erro(_msg_rede(e))
    except KeyboardInterrupt:
        print()
        return _erro('interrompido. Os meses ja baixados ficaram em cache; rode de novo para continuar.', 130)
    return 0


def cmd_exemplo(a):
    import calculadora
    import radar
    import sicor
    print('=' * 70)
    print('1) CALCULADORA com dados ficticios')
    print('=' * 70)
    with open(os.path.join(EXEMPLOS, 'simulacao_ficticia.json'), encoding='utf-8') as f:
        ex = json.load(f)
    lead, banco = ex.pop('lead'), ex.pop('banco')
    ex.pop('_aviso', None)
    pasta_calc = os.path.join(SAIDA, 'calculadora')
    calculadora.gerar_pagina(None, pasta_calc)
    print()
    calculadora.gerar_simulacao(ex, lead, banco, pasta_calc)

    print()
    print('=' * 70)
    print('2) RADAR com dados ficticios (formato do relatorio, sem internet)')
    print('=' * 70)
    radar.gerar_exemplo(os.path.join(EXEMPLOS, 'radar_ficticio.json'), os.path.join(SAIDA, 'radar'))

    print()
    print('=' * 70)
    print('3) Teste de acesso a API Olinda do Banco Central (radar real)')
    print('=' * 70)
    if a.sem_rede:
        print('Pulado (--sem-rede).')
    else:
        try:
            sicor.testar_conexao(timeout=a.timeout)
            print('API Olinda acessivel. Para o radar real: python main.py radar --uf <UF> [--ano AAAA]')
        except sicor.ErroSicor as e:
            print(_msg_rede(e))
            print('(O exemplo segue OK: calculadora e radar ficticio nao dependem de internet.)')
    print('\nExemplo concluido. Arquivos em:', SAIDA)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog='main.py',
        description='Ferramentas AGRO - calculadora do credito rural e radar SICOR (Banco Central).')
    sub = ap.add_subparsers(dest='cmd', required=True)

    c = sub.add_parser('calculadora', help='pagina interativa + simulacao pronta para o lead',
                       description='Gera saida/calculadora/index.html (pagina interativa). Com --valor/--taxa/'
                                   '--parcelas gera tambem a simulacao do lead (HTML + TXT para WhatsApp). '
                                   'Valores aceitam 850000, 850000.50 ou 850.000,50.')
    c.add_argument('--valor', help='valor financiado ou saldo devedor (R$)')
    c.add_argument('--taxa', help='taxa de juros da cedula (ex.: 12,5)')
    c.add_argument('--taxa-tipo', choices=['aa', 'am'], default='aa', help='aa = %% ao ano (padrao), am = %% ao mes')
    c.add_argument('--parcelas', type=int, help='numero de parcelas')
    c.add_argument('--periodicidade', choices=['anual', 'semestral', 'mensal'], default='anual')
    c.add_argument('--sistema', choices=['price', 'sac'], default='price')
    c.add_argument('--carencia', type=int, default=0, help='meses ate a 1a parcela do principal')
    c.add_argument('--carencia-juros', choices=['pagos', 'capitalizados'], default='pagos')
    c.add_argument('--custos', help='tarifas, seguros e IOF descontados na liberacao (R$)')
    c.add_argument('--taxa-comparacao', help='comparar com outra taxa (mesma unidade)')
    c.add_argument('--prorrogar-anos', type=int, default=0, help='cenario de prorrogacao: anos a mais no prazo')
    c.add_argument('--prorrogar-carencia', type=int, default=0, help='meses de carencia a mais no cenario prorrogado')
    c.add_argument('--lead', help='nome do lead (aparece no relatorio)')
    c.add_argument('--banco', help='banco/cooperativa (aparece no relatorio)')
    c.add_argument('--whatsapp', help='numero do botao da pagina, so digitos com DDI (ex.: 5500000000000)')
    c.add_argument('--saida', help='pasta de saida (padrao: AGRO/saida/calculadora)')

    r = sub.add_parser('radar', help='ranking de municipios/regioes por credito rural (SICOR/BCB)',
                       description='Baixa os contratos de credito rural do SICOR (API Olinda do Banco Central) '
                                   'e ranqueia municipios e mesorregioes. Precisa de internet.')
    r.add_argument('--uf', required=True, help='UF(s) alvo, ex.: GO ou GO,MT,MS; TODAS = Brasil inteiro')
    r.add_argument('--ano', type=int, help='ano de emissao (padrao: ano anterior)')
    r.add_argument('--municipio', help='filtrar o relatorio a estes municipios (separados por virgula); '
                                       'a posicao continua sendo o ranking da(s) UF(s)')
    r.add_argument('--produtos', help='produtos de foco do indice, ex.: SOJA,MILHO,BOVINOS '
                                      '(padrao: config_comercial.py; vazio "" = nenhum)')
    r.add_argument('--timeout', type=int, default=150, help='segundos por consulta (padrao 150)')
    r.add_argument('--tentativas', type=int, default=5, help='tentativas por consulta (padrao 5)')
    r.add_argument('--saida', help='pasta de saida (padrao: AGRO/saida/radar)')

    e = sub.add_parser('exemplo', help='roda tudo com dados ficticios (funciona sem internet)')
    e.add_argument('--sem-rede', action='store_true', help='nem tenta acessar a API do Banco Central')
    e.add_argument('--timeout', type=int, default=15, help='segundos do teste de acesso a API (padrao 15)')

    a = ap.parse_args(argv)
    return {'calculadora': cmd_calculadora, 'radar': cmd_radar, 'exemplo': cmd_exemplo}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
