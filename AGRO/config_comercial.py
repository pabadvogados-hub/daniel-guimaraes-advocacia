"""
Configuracao das ferramentas AGRO - Daniel Guimaraes Advocacia.

Tudo que o escritorio decide mora aqui: dados que aparecem na calculadora enviada ao lead,
cores da marca e os pesos do radar de credito rural.

Campos com '[PREENCHER]' ainda nao foram definidos pelo escritorio. Enquanto estiverem assim,
eles NAO aparecem nas paginas geradas (o rodape mostra so o que estiver preenchido) e o botao
do WhatsApp da calculadora fica desligado.

Obs.: o arquivo se chama config_comercial.py (e nao config.py) para nao conflitar com a pasta
config/ que existe na raiz do projeto.
"""

PREENCHER = '[PREENCHER]'

# ============================================================
# ESCRITORIO
# ============================================================
ESCRITORIO = {
    'nome': 'Daniel Guimarães Advocacia',
    'responsavel': 'Dr. Daniel Guimarães',
    'oab': PREENCHER,             # ex.: 'OAB/UF 00.000'
    'cnpj': PREENCHER,
    'cidade_uf': PREENCHER,       # ex.: 'Cidade/UF'
    'endereco': PREENCHER,
    'telefone': PREENCHER,        # ex.: '(00) 00000-0000'
    'site': PREENCHER,            # ex.: 'www.dominio.com.br'
    'instagram': PREENCHER,       # ex.: '@perfil'
    'nicho': 'Defesa do produtor rural em dívidas com bancos e cooperativas',
}

# ============================================================
# MARCA (cores neutras: azul-marinho + verde-oliva)
# ============================================================
CORES = {
    'marinho': '#1F2A44',         # cor principal (topo, titulos, tabelas)
    'marinho_claro': '#2E3B5C',
    'oliva': '#6B7F3A',           # cor de destaque (bordas, juros, botoes)
    'oliva_escuro': '#55662D',
    'oliva_claro': '#EEF1E4',     # fundo de destaque
    'papel': '#F7F8F5',
    'linha': '#DCE0D3',
    'suave': '#5F6672',
    'texto': '#232833',
    'whatsapp': '#15803D',
    'whatsapp_escuro': '#106B31',
}

# ============================================================
# CALCULADORA (pagina/relatorio enviado ao lead)
# ============================================================

# Numero do WhatsApp do botao da calculadora: so digitos, com DDI 55 (ex.: 5500000000000).
# Vazio ou [PREENCHER] = botao desligado (a pagina mostra o aviso para contato pelos canais do escritorio).
WHATSAPP_CALCULADORA = PREENCHER
MENSAGEM_WHATSAPP_CALCULADORA = ('Olá! Usei a calculadora de crédito rural e gostaria de conversar '
                                 'com a equipe do escritório sobre a minha dívida rural.')

# ============================================================
# RADAR DE CREDITO RURAL (SICOR / Banco Central)
# ============================================================
RADAR = {
    # pesos do indice de prioridade (somam 1)
    'peso_contratos': 0.40,       # quantidade de contratos = quantidade de produtores com credito
    'peso_valor': 0.35,           # volume financiado = tamanho das dividas (ticket)
    'peso_foco': 0.25,            # volume de custeio nos produtos de foco abaixo
    # produtos de foco (nome exato do SICOR, em maiusculas). Cada produto = 12 consultas a mais por UF.
    'produtos_foco': ['SOJA', 'BOVINOS'],
    'top_sugestao': 15,           # quantos municipios sugerir para anuncio/prospeccao
}


def preenchido(valor):
    """True se o campo tem valor real (nao vazio e nao '[PREENCHER]')."""
    v = (valor or '').strip()
    return bool(v) and PREENCHER not in v
