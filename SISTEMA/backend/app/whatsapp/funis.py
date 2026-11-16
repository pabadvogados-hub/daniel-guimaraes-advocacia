"""Funis (quadros) do CRM do Daniel Guimarães Advocacia — fonte única de nomes, IDs e colunas.

Os IDs são FIXOS de propósito: o seed cria cada quadro com o id abaixo, e os robôs (SYNC/*)
e as telas filtram por esses números. Num banco novo, sem id fixo, o primeiro quadro viraria
o 1 e todo filtro por id apontaria para o lugar errado.

Operação (nicho: defesa do produtor rural contra bancos):
- Linha FIXA do escritório  -> PRODUTORES RURAIS (constante RECLAMANTES, id 10), atendida pela SDR de IA.
- Número do Dr. Titular     -> EMPRESAS (cooperativas, revendas, agroindústrias e empresas do agro).
- Palestra / evento rural   -> funil próprio (id 31, grupo com aquecimento).
O nome das CONSTANTES (RECLAMANTES, PALESTRA...) e os IDs ficaram os da base porque robôs e telas
importam por eles; só os NOMES exibidos e as colunas de campanha mudaram.
"""

# ---------------- IDs ----------------
RECLAMANTES = 10        # entrada e qualificação do PRODUTOR RURAL até o contrato
CLIENTES = 11           # cliente com processo/atendimento em curso
PRODUCAO = 18           # esteira da inicial: documentos -> produção -> revisão -> distribuição
CONTRATACAO = 20        # contrato, documentos e assinatura
EMPRESAS = 30           # linha B2B do Dr. Titular (empresas do agro)
PALESTRA = 31           # funil da palestra / evento rural

# ---------------- Nomes ----------------
NOME = {
    RECLAMANTES: 'Produtores Rurais',
    CLIENTES: 'Clientes',
    PRODUCAO: 'Produção',
    CONTRATACAO: 'Contratação',
    EMPRESAS: 'Empresas',
    PALESTRA: 'Palestra Crédito Rural',
}
PIPE_LEADS = NOME[RECLAMANTES]
PIPE_CLIENTES = NOME[CLIENTES]
PIPE_PRODUCAO = NOME[PRODUCAO]
PIPE_CONTRATACAO = NOME[CONTRATACAO]
PIPE_EMPRESAS = NOME[EMPRESAS]
PIPE_PALESTRA = NOME[PALESTRA]

# ---------------- Colunas de entrada por campanha (Produtores Rurais) ----------------
# O lead de campanha cai direto na coluna da origem; os robôs tratam todas como entrada.
CAIXA = 'Caixa de Entrada'
CAMPANHA_PRORROGACAO = 'Campanha Prorrogação'            # safra frustrou / parcela não fecha
CAMPANHA_EXECUCAO = 'Campanha Execução e Leilão'         # execução de cédula, leilão de terra
CAMPANHA_APREENSAO = 'Campanha Busca e Apreensão'        # máquina/veículo financiado
CAMPANHA_GERAL = 'Campanha Geral'
ETAPAS_ENTRADA = (CAIXA, CAMPANHA_PRORROGACAO, CAMPANHA_EXECUCAO, CAMPANHA_APREENSAO, CAMPANHA_GERAL)

# Origem (campo conversa.origem) -> coluna de entrada.
ORIGEM_PARA_COLUNA = {
    CAMPANHA_PRORROGACAO: CAMPANHA_PRORROGACAO,
    CAMPANHA_EXECUCAO: CAMPANHA_EXECUCAO,
    CAMPANHA_APREENSAO: CAMPANHA_APREENSAO,
    CAMPANHA_GERAL: CAMPANHA_GERAL,
}

# Frase exclusiva de cada anúncio (mensagem pré-preenchida do clique para o WhatsApp).
# Ajuste aqui quando as campanhas forem criadas; comparação sem acento e em minúsculas.
FRASES_CAMPANHA = {
    CAMPANHA_PRORROGACAO: ('quero prorrogar minha divida', 'prorrogacao da divida rural', 'perdi a safra',
                           'a safra frustrou', 'alongamento da divida'),
    CAMPANHA_EXECUCAO: ('o banco esta me executando', 'execucao da cedula', 'leilao da minha terra',
                        'leilao da fazenda', 'meu imovel vai a leilao'),
    CAMPANHA_APREENSAO: ('busca e apreensao', 'tomaram meu trator', 'o banco quer tomar minha maquina'),
    CAMPANHA_GERAL: ('quero falar sobre minha divida rural', 'divida com o banco'),
    'Campanha Palestra': ('palestra', 'evento do credito rural'),
}

QUENTE = 'Lead Quente'
QUALIFICADO = 'Lead Qualificado'
DESQUALIFICADO = 'Lead Desqualificado'
CONTRATO = 'Contrato / Assinatura'

COLUNAS = {
    RECLAMANTES: [
        CAIXA, CAMPANHA_PRORROGACAO, CAMPANHA_EXECUCAO, CAMPANHA_APREENSAO, CAMPANHA_GERAL,
        QUENTE, QUALIFICADO, 'Contatado', 'Pré fechamento [fluxo aquecimento]', 'Em Negociação',
        'Pós-Reunião de Fechamento', CONTRATO, 'Ganho', DESQUALIFICADO,
        'Perdido - Sem resposta', 'Perdido - Sem interesse', 'Perdido',
    ],
    CONTRATACAO: [
        'Fechou! Boas vindas e Documentos para contrato', 'Fase de Contratação', 'Contrato no ZapSign',
        'Assinado', 'Ligação: reaquecimento de documentos', 'Perdido',
    ],
    PRODUCAO: ['Aguardando Documentos', 'Producao da Inicial', 'Revisao', 'Distribuicao', 'Distribuida'],
    CLIENTES: ['Novo Cliente', 'Em Atendimento', 'Processo Ativo [Cliente ou funcionario]', 'Resolvido'],
    EMPRESAS: [
        CAIXA, 'Diagnóstico', 'Reunião Marcada', 'Proposta Enviada', 'Negociação', 'Cliente Ativo', 'Perdido',
    ],
    PALESTRA: [
        'Captação', 'No Grupo (aquecimento)', 'Confirmou Presença', 'Assistiu à Palestra', 'Não Compareceu',
        'Triagem', CONTRATO, 'Ganho', 'Perdido',
    ],
}

# Ordem em que aparecem no CRM. O primeiro é o padrão da linha de produtores rurais.
ORDEM = [RECLAMANTES, CONTRATACAO, PRODUCAO, CLIENTES, EMPRESAS, PALESTRA]

# Esteira que a automação pode AVANÇAR mesmo com o quadro fixado por gente.
ESTEIRA = [PIPE_LEADS, PIPE_CONTRATACAO, PIPE_PRODUCAO]

# Quadro padrão de cada agente (linha). Conversa nova nasce aqui.
QUADRO_DO_AGENTE = {'reclamante': RECLAMANTES, 'empresas': EMPRESAS}


def coluna_da_origem(origem: str):
    """Coluna de entrada para a origem da campanha, ou None (cai na Caixa de Entrada)."""
    return ORIGEM_PARA_COLUNA.get((origem or '').strip())


def origem_pela_frase(texto: str):
    """Descobre a campanha pela frase do anúncio. None se nenhuma bater."""
    import unicodedata
    t = unicodedata.normalize('NFKD', (texto or '').lower()).encode('ascii', 'ignore').decode()
    for origem, frases in FRASES_CAMPANHA.items():
        for f in frases:
            f2 = unicodedata.normalize('NFKD', f.lower()).encode('ascii', 'ignore').decode()
            if f2 in t:
                return origem
    return None
