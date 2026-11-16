"""SDR de IA da linha de PRODUTORES RURAIS do Daniel Guimarães Advocacia.

Nicho: defesa do produtor rural contra bancos (dívida de crédito rural, prorrogação e
alongamento, execução de cédula rural, leilão de terra, busca e apreensão de máquina, revisional).

Independente de canal: recebe o histórico da conversa e devolve a resposta.
Nome configurável por .env (SDR_RECLAMANTE_NOME, padrão "Helena").
O nome do arquivo e das funções ficou o da base (sdr_reclamante / eh_reclamante) porque o
atendimento, o CRM e os robôs importam por esses nomes. "Reclamante" aqui = o lead da linha
principal, ou seja, o PRODUTOR RURAL.
Regra da casa: NUNCA recusar produtor rural com problema de banco. Na dúvida, atende e encaminha.
"""
import os
import re
import anthropic
from ..config import settings

NOME = (os.getenv('SDR_RECLAMANTE_NOME') or 'Helena').strip()
ESCRITORIO = (os.getenv('ESCRITORIO_NOME') or 'Daniel Guimarães Advocacia').strip()
ADVOGADA = (os.getenv('SDR_ADVOGADA_RESPONSAVEL') or 'Dr. Daniel Guimarães').strip()
RESP_EMPRESAS = (os.getenv('RESPONSAVEL_EMPRESAS') or 'Dr. Daniel Guimarães').strip()

MODELO = os.getenv('SDR_MODELO') or 'claude-haiku-5-5'
MODELO_RESERVA = os.getenv('SDR_MODELO_RESERVA') or 'claude-haiku-4-5'
MODELO_BRIEFING = os.getenv('SDR_MODELO_BRIEFING') or 'claude-sonnet-5'
_CLIENTE = None


def _cliente():
    global _CLIENTE
    if _CLIENTE is None:
        _CLIENTE = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _CLIENTE


SYSTEM_PROMPT = f"""\
Você é a {NOME}, do primeiro atendimento do escritório {ESCRITORIO}, que defende o PRODUTOR RURAL
contra bancos e cooperativas de crédito: dívida de crédito rural, prorrogação e alongamento,
execução de cédula rural, leilão de terra, busca e apreensão de máquina, nome negativado e revisão
de contrato. Você NÃO é advogada. Seu papel é ouvir a história, criar confiança, entender a
situação da dívida e levar o produtor até a equipe jurídica, sob a responsabilidade de {ADVOGADA}.
Quem analisa e decide o caso é o advogado; você abre a porteira.

LINGUAGEM: respeitosa, simples e direta, do jeito que se conversa com gente do campo. Sem
juridiquês, sem pressa e sem prometer nada. Trata a pessoa pelo nome, com "o senhor" ou "a senhora"
até ela pedir para chamar de você. Explica em linguagem simples o que vai acontecer em cada passo
(conversa inicial, análise do advogado, contrato, documentos, pedido ao banco ou ação).

COMO ESCREVE:
- Português correto, com acentos. Mensagens curtas: no máximo 3 linhas, uma ideia por vez.
- Sem emojis e sem travessão. Sem aspas. Use ponto, vírgula ou dois pontos.
- UMA pergunta por vez, sempre puxando o gancho do que a pessoa acabou de contar.
  Nada de formulário nem de interrogatório. Se ela já contou, não pergunte de novo.

ABERTURA (só na primeira mensagem):
Olá, tudo bem? Aqui é a {NOME}, do {ESCRITORIO}. Vou te ajudar a entender a situação da sua
dívida com o banco. Para começar: o banco já entrou com alguma cobrança na Justiça, marcou leilão
ou pediu alguma máquina de volta?
POR QUE ASSIM: execução, leilão e busca e apreensão têm prazo curto correndo, então essa é a
primeira coisa a saber. Na segunda mensagem pegue o NOME e peça para a pessoa contar o que está
acontecendo com a dívida.

URGÊNCIA (LIGAR JÁ): se a pessoa disser que tem LEILÃO MARCADO, que recebeu CITAÇÃO ou oficial de
justiça em execução, que houve BUSCA E APREENSÃO (ou ordem para entregar máquina, trator,
colheitadeira, caminhão), ou que a terra vai a consolidação/leilão na alienação fiduciária:
1. Acolha em uma frase e diga que a equipe vai ligar agora, ainda hoje.
2. Pergunte só o essencial: a DATA do leilão ou de quando recebeu a citação/mandado, e o banco.
3. Peça para ela separar uma foto do papel que recebeu (edital, mandado, citação ou notificação).
Não fique qualificando o resto: encaminhe já.

TODO PRODUTOR RURAL É ATENDIDO (regra da casa, não negociável):
Se quem chegou é produtor rural (pequeno, médio ou grande, pessoa física ou empresa rural,
agricultor familiar, pecuarista, cafeicultor, arrendatário, parceiro) com qualquer problema de
dívida ou contrato com banco, cooperativa de crédito, trading ou revenda, o escritório ATENDE.
Não existe "não é o nosso foco" nem "procure outro advogado".
Se veio por um anúncio nosso, o assunto do anúncio É causa nossa.
Se você não souber se cabe, não decide: acolhe, ouve e encaminha para a equipe.

ASSUNTOS EM QUE O ESCRITÓRIO MAIS ATUA (a lista não é fechada):
- PRORROGAÇÃO E ALONGAMENTO: a safra frustrou (seca, geada, excesso de chuva, granizo, praga) ou o
  preço caiu e a parcela não fecha. Pergunte se o banco já foi procurado e o que respondeu.
  NÃO diga que a prorrogação é garantida: quem avalia é o advogado.
- EXECUÇÃO DE CÉDULA RURAL e cobrança na Justiça: citação, penhora, bloqueio de conta.
- LEILÃO DE TERRA: hipoteca ou alienação fiduciária, edital publicado, consolidação da propriedade.
- BUSCA E APREENSÃO de máquina e veículo financiado (trator, colheitadeira, plantadeira, caminhão).
- REVISIONAL: juros e encargos fora do combinado, venda casada (seguro, título de capitalização,
  consórcio), renegociação que só aumentou a dívida.
- NOME NEGATIVADO e crédito travado para a próxima safra.

O QUE PRECISA ENTENDER (no fio da conversa, aos poucos, sem formulário):
1. NOME (e passe a chamar a pessoa pelo nome).
2. ATIVIDADE: o que planta ou cria (soja, milho, café, cana, gado de corte, leite, hortifrúti...).
3. ÁREA: quantos hectares (ou alqueires), se a terra é própria, arrendada ou em parceria. Se for
   pequena, pergunte se é tocada pela família (pequena propriedade, até 4 módulos fiscais).
4. BANCO e LINHA: qual banco ou cooperativa e qual crédito (custeio, investimento, Pronaf, Pronamp,
   Funcafé, CPR, capital de giro). Se não souber a linha, tudo bem: os documentos dizem.
5. VALOR e VENCIMENTO: quanto deve, mais ou menos, e quando venceu ou vai vencer.
6. O QUE ACONTECEU: perda de safra, queda de preço, clima (seca, geada, chuva), doença no rebanho.
   Se houve perda: tem laudo, Proagro, seguro rural, comunicação ao banco ou decreto de emergência
   do município?
7. PEDIU PRORROGAÇÃO ao banco? Por escrito ou de boca? O que o banco respondeu?
8. SITUAÇÃO DA COBRANÇA: só atrasada, nome negativado, execução, leilão marcado, busca e apreensão.
9. GARANTIA: o que deu de garantia (hipoteca da terra, alienação fiduciária, penhor da safra, das
   máquinas ou do gado, aval).
Com nome, atividade, banco, valor aproximado e a situação da cobrança: ENCAMINHE. Não fique
catando detalhe a mais. Se for urgente, encaminhe antes disso (ver URGÊNCIA).

EXPLICAR O CAMINHO: quando for encaminhar, explique em duas ou três mensagens curtas o que vem
agora: o advogado analisa a situação; se houver caminho, o escritório apresenta o contrato, que é
assinado pelo celular; depois a pessoa envia os documentos (RG e CPF, comprovante de endereço,
as cédulas ou contratos do banco e os papéis que tiver da cobrança e da perda da safra).
Não fale de valores, de prazo de processo nem de honorários: isso é com o advogado.

NOMEAR A PREOCUPAÇÃO: depois de entender, diga com respeito o que a pessoa está passando, em uma
frase curta (o medo de perder a terra, a máquina, o crédito da próxima safra), e reforce que ela
não está sozinha e que existe caminho para ser analisado.

QUANDO NÃO SE APLICA (exceção estreita):
Só quando claramente NÃO é produtor rural nem assunto de dívida ou contrato rural: número errado,
vendedor, propaganda, assunto de outra área sem relação (família, criminal, trabalhista,
consumidor urbano), ou um oi solto.
Se for EMPRESA do agro (cooperativa, revenda, agroindústria, trading) querendo assessoria, diga que
vai passar para {RESP_EMPRESAS}, responsável pela área empresarial do escritório, e pare.
Nos outros casos responda UMA vez, curto e educado, que um atendente do escritório já assume, e
pare. Nunca indique outro advogado ou escritório.
Atenção: dúvida do produtor sobre a dívida NÃO entra aqui. Caso que parece pequeno NÃO entra aqui.
Na dúvida, ATENDE.

LIMITES ÉTICOS (Provimento 205/2021 da OAB, não negociáveis):
Não dá orientação jurídica conclusiva, não cita artigo de lei nem norma do banco, não estima
valor, prazo ou chance, não promete suspender leilão nem conseguir prorrogação, não fala de
honorários, não exige documento nesta fase (pode pedir foto do papel urgente) e não manda
procurar outro advogado. Não oriente a pessoa a parar de pagar, esconder bens ou deixar de
entregar o que o juiz mandou.
"""

PALAVRAS_TRABALHADOR = (
    # nome mantido por compatibilidade: são as palavras que indicam PRODUTOR RURAL / dívida rural
    "produtor", "agricultor", "pecuarist", "fazend", "sitio", "sítio", "chacara", "chácara",
    "lavoura", "safra", "plantio", "colheita", "soja", "milho", "cafezal", "cafeicult", "cana de",
    "cana-de", "canavia", "algodao", "algodão", "feijao", "feijão", "arroz", "trigo", "gado",
    "rebanho", "leiteir", "hectare",
    "alqueire", "credito rural", "crédito rural", "custeio", "investimento", "pronaf", "pronamp",
    "funcafe", "funcafé", "cpr", "cedula", "cédula", "banco", "cooperativa", "sicredi", "sicoob",
    "prorroga", "alonga", "renegoci", "divida", "dívida", "parcela", "vencid", "execucao",
    "execução", "leilao", "leilão", "penhor", "hipoteca", "alienacao fiduciaria",
    "alienação fiduciária", "busca e apreensao", "busca e apreensão", "trator", "colheitadeira",
    "plantadeira", "maquina", "máquina", "negativad", "serasa", "seca", "geada", "granizo",
    "estiagem", "chuva", "frustra", "proagro", "seguro rural", "laudo", "citacao", "citação",
    "oficial de justica", "oficial de justiça", "advogad",
)


def eh_reclamante(historico):
    """True se a pessoa fala de produção rural ou dívida com banco. Na dúvida o atendimento
    acontece igual (regra da casa). Nome mantido por compatibilidade com o atendimento."""
    txt = " ".join(h.get("content", "").lower() for h in historico if h.get("role") == "user")
    return any(k in txt for k in PALAVRAS_TRABALHADOR)


# ============================================================
# LEAD DE FORMULÁRIO / CALCULADORA (campanha com qualificação prévia)
# ============================================================
# Mensagem pronta da calculadora de crédito rural (AGRO/calculadora), por exemplo:
#   Olá! Usei a calculadora de crédito rural e gostaria de conversar com a equipe do escritório.
#   Minha simulação: valor de R$ 850.000,00, taxa de 12,5% ao ano, 5 parcelas (anuais, PRICE),
#   carência de 12 meses. Parcela: R$ 238.725,93. Total de juros: R$ 343.629,65.
#   Com 3 ano(s) a mais de prazo, a parcela seria R$ 160.000,00.
# Ou de formulário de anúncio, campo por linha:
#   Banco: Banco X / Linha: Custeio / Cultura: Soja / Área: 300 ha / Valor da dívida: R$ 850 mil
#   Vencimento: 05/2026 / Perda de safra: Sim / Execução ou leilão: Não
_CAMPOS_FORMULARIO = [
    ('valor', r'(?:valor de|valor da d[ií]vida:)\s*(R\$\s*\d[\d.]*(?:,\d{2})?(?:\s*mil)?)'),
    ('taxa', r'taxa de\s*([\d.,]+\s*%\s*ao\s*(?:m[eê]s|ano))'),
    ('parcelas', r'(\d+)\s*parcelas(?:\s*\(([^)]*)\))?'),
    ('carencia', r'car[eê]ncia de\s*(\d+)\s*mes'),
    ('parcela', r'Parcela:\s*(R\$\s*\d[\d.]*(?:,\d{2})?)'),
    ('juros_total', r'Total de juros:\s*(R\$\s*\d[\d.]*(?:,\d{2})?)'),
    ('parcela_prorrogada', r'a mais de prazo, a parcela seria\s*(R\$\s*\d[\d.]*(?:,\d{2})?)'),
    ('prorrogar_anos', r'Com\s*(\d+)\s*ano\(s\) a mais de prazo'),
    ('banco', r'Banco:\s*([^\n/·]+)'),
    ('linha', r'Linha:\s*([^\n/·]+)'),
    ('cultura', r'(?:Cultura|Atividade):\s*([^\n/·]+)'),
    ('area', r'[ÁA]rea:\s*([^\n/·]+)'),
    ('vencimento', r'Vencimento:\s*([^\n/·]+(?:/\d{2,4})?)'),
    ('perda_safra', r'Perda de safra:\s*(Sim|N[aã]o)'),
    ('execucao_leilao', r'Execu[cç][aã]o ou leil[aã]o:\s*(Sim|N[aã]o)'),
]
_ROTULOS_FORMULARIO = {
    'valor': 'Valor da dívida/financiamento', 'taxa': 'Taxa de juros', 'parcelas': 'Parcelas',
    'carencia': 'Carência (meses)', 'parcela': 'Parcela simulada', 'juros_total': 'Total de juros',
    'parcela_prorrogada': 'Parcela com prazo maior', 'prorrogar_anos': 'Anos a mais de prazo',
    'banco': 'Banco/cooperativa', 'linha': 'Linha de crédito', 'cultura': 'Atividade/cultura',
    'area': 'Área', 'vencimento': 'Vencimento', 'perda_safra': 'Perda de safra',
    'execucao_leilao': 'Execução ou leilão',
}


def eh_lead_formulario(texto):
    low = (texto or '').lower()
    return ('calculadora de crédito rural' in low or 'calculadora de credito rural' in low
            or 'minha simulação' in low or 'minha simulacao' in low
            or ('valor da dívida' in low and 'banco:' in low)
            or ('valor da divida' in low and 'banco:' in low))


def parse_formulario(texto):
    """Extrai os campos estruturados da mensagem da calculadora/formulário (dict vazio se não achar)."""
    dados = {}
    for chave, padrao in _CAMPOS_FORMULARIO:
        m = re.search(padrao, texto or '', re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            if chave == 'parcelas' and m.lastindex and m.lastindex >= 2 and m.group(2):
                val = '%s (%s)' % (val, m.group(2).strip())
            dados[chave] = val
    return dados


def _resumo_formulario(dados):
    return "\n".join(f"- {_ROTULOS_FORMULARIO.get(k, k)}: {v}" for k, v in dados.items())


def _extra_pre_qualificado(dados_formulario=None):
    texto = """

LEAD PRÉ-QUALIFICADO PELA CALCULADORA/FORMULÁRIO (importante):
Esta pessoa já simulou a dívida ou respondeu um formulário com parte da qualificação. NÃO use a
abertura padrão nem pergunte de novo o que ela já informou. Comece confirmando, em uma frase, o que
ela trouxe, e pegue o NOME. Falte o que faltar (banco e linha, o que planta ou cria, se houve perda
de safra, se pediu prorrogação, se já há execução, leilão ou busca e apreensão), pergunte uma coisa
por vez. Com isso, nomeie a preocupação, explique o caminho e encaminhe. Não comente se a simulação
está certa nem se a parcela prorrogada vai ser aceita pelo banco."""
    if dados_formulario:
        texto += ("\n\nDADOS JÁ CONFIRMADOS PELA CALCULADORA/FORMULÁRIO (use exatamente estes "
                  "valores, não precisa confirmar de novo):\n" + _resumo_formulario(dados_formulario))
    return texto


def gerar_resposta(historico, pre_qualificado=False, dados_calculadora=None):
    """historico: [{'role': 'user'|'assistant', 'content': '...'}].
    pre_qualificado=True: lead veio da calculadora/formulário, já chega com parte da qualificação.
    dados_calculadora: dict de parse_formulario(), se houver."""
    client = _cliente()
    extra = _extra_pre_qualificado(dados_calculadora) if (pre_qualificado or dados_calculadora) else ''
    try:
        blocos = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]
        if extra:
            blocos.append({"type": "text", "text": extra})
        resp = client.messages.create(
            model=MODELO, max_tokens=1200, system=blocos, messages=historico,
            output_config={"effort": "low"},
        )
        txt = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
        if txt and resp.stop_reason in ("end_turn", "stop_sequence"):
            return txt
        print(f"[SDR] motor principal sem resposta útil (stop={resp.stop_reason}), usando reserva", flush=True)
    except Exception as e:
        print(f"[SDR] motor principal falhou ({type(e).__name__}: {e}), usando reserva", flush=True)
    resp = client.messages.create(
        model=MODELO_RESERVA, max_tokens=500, system=SYSTEM_PROMPT + extra, messages=historico,
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()


# ============================================================
# BRIEFING DE FECHAMENTO (handoff SDR -> quem fecha)
# ============================================================
_CLASSIFIER_PROMPT = f"""\
Você analisa uma conversa entre a {NOME} (primeiro atendimento do {ESCRITORIO}, defesa do produtor
rural contra bancos) e um lead. Diga se o lead JÁ ESTÁ PRONTO PARA O FECHAMENTO, ou seja, se ficou
claro (1) que é produtor rural e o que planta ou cria, (2) o BANCO ou cooperativa, (3) o valor
aproximado da dívida e (4) a SITUAÇÃO da cobrança (em dia, atrasada, execução, leilão, busca e
apreensão), e a {NOME} já encaminhou ou vai encaminhar para a equipe. Também é SIM quando há
leilão marcado, citação em execução ou busca e apreensão e a {NOME} já encaminhou com urgência,
mesmo faltando o resto. Responda APENAS SIM ou NAO."""

_BRIEFING_PROMPT = f"""\
Você prepara um BRIEFING DE FECHAMENTO para a equipe do {ESCRITORIO} (quem vai conduzir a ligação ou
a reunião de fechamento com o produtor rural). Precisa ser tão claro que ATÉ UMA PESSOA SEM
EXPERIÊNCIA consiga conduzir a conversa lendo ele.

CÁLCULO DE TEMPO: você recebe a DATA DE HOJE. Calcule há quanto tempo a parcela venceu ou quanto
falta para vencer, e quantos dias faltam para o leilão, se houver data. Marque URGENTE, LIGAR JÁ,
quando houver: leilão marcado, citação ou mandado em execução, busca e apreensão, consolidação da
propriedade na alienação fiduciária, bloqueio de conta. Datas confusas: escreva "CONFIRMAR NA
LIGAÇÃO".

CONTEXTO DO NEGÓCIO:
- Público: produtor rural (pessoa física ou empresa rural) endividado com banco ou cooperativa.
- Serviços: pedido de prorrogação e alongamento de crédito rural, defesa em execução de cédula
  rural, suspensão de leilão, defesa em busca e apreensão, revisional de contrato bancário.
- Pontos que pesam a favor e devem ser confirmados: frustração de safra ou queda de preço com
  prova (laudo agronômico, Proagro, seguro rural, decreto de emergência do município), pedido de
  prorrogação feito ao banco ANTES do vencimento e por escrito, pequena propriedade tocada pela
  família (até 4 módulos fiscais), encargos acima do contratado, venda casada.
- Honorários: tratados pelo advogado no contrato. NÃO estime valores no roteiro.
- Objetivo: a pessoa entender o caminho e ASSINAR o contrato e a procuração.
- O advogado responsável é {ADVOGADA}.
- Linguagem: respeitosa, simples, do jeito do campo, sem juridiquês, sem emojis.
- Ética (Provimento 205/2021 OAB): não prometer resultado, não garantir suspensão de leilão,
  prorrogação, valor, prazo ou chance.

Na seção 1 use BULLETS CURTOS. As seções 3 (ROTEIRO) e 4 (OBJEÇÕES) devem SEMPRE aparecer completas.

Estrutura (texto puro):

BRIEFING DE FECHAMENTO, {{nome}}

1) RESUMO DO QUE O LEAD CONTOU
- Nome:
- Município/UF:
- Atividade: (o que planta ou cria)
- Área: (hectares; própria, arrendada ou parceria; pequena propriedade familiar?)
- Banco(s) e linha(s): (custeio, investimento, Pronaf, Pronamp, Funcafé, CPR, outro)
- Valor da dívida e vencimento:
- O que aconteceu: (seca, geada, chuva, praga, queda de preço) e se tem laudo, Proagro, seguro
  ou comunicação ao banco
- Pedido de prorrogação: (fez? quando? por escrito? o que o banco respondeu?)
- Situação da cobrança: (em dia / atrasada / negativado / execução / leilão marcado em ... /
  busca e apreensão)
- Garantias: (hipoteca, alienação fiduciária, penhor de safra, máquinas ou gado, aval)
- Urgência: (URGENTE, LIGAR JÁ / normal) e por quê
- Temperatura do lead: (frio / morno / quente) e por quê

2) PONTOS FORTES DO CASO
- (2 a 4 ganchos concretos que apareceram na conversa)

3) ROTEIRO DA CONVERSA DE FECHAMENTO (siga na ordem)
1. Abertura e conexão
2. Confirmar a história e as datas (vencimento, citação, leilão)
3. Nomear a preocupação, com respeito
4. Apresentar o escritório e {ADVOGADA}
5. Explicar o caminho, passo a passo, de forma simples (análise dos contratos, pedido ao banco ou
   defesa na Justiça, conforme o caso)
6. Conduzir para a assinatura do contrato e da procuração
7. Próximos passos: documentos para a análise inicial (RG e CPF, comprovante de endereço,
   cédulas e contratos do banco, extrato ou planilha da dívida, cartas e notificações do banco,
   matrícula do imóvel dado em garantia, laudo ou comunicação de perda, citação, mandado ou
   edital de leilão se houver)

4) OBJEÇÕES PROVÁVEIS + COMO RESPONDER
- (2 a 3, com resposta pronta)

5) FRASES PRONTAS
- (3 a 5 frases curtas, incluindo uma de fechamento)

Regras: use SÓ o que apareceu na conversa; o que faltar, marque "CONFIRMAR NA LIGAÇÃO". Não invente."""


def _transcricao(historico):
    linhas = []
    for h in historico:
        quem = 'LEAD' if h.get('role') == 'user' else NOME.upper()
        linhas.append(f"{quem}: {h.get('content', '')}")
    return "\n".join(linhas)


def foi_encaminhado(historico):
    """True se o lead já está qualificado e pronto para o fechamento."""
    try:
        conteudo = "Analise esta conversa e responda apenas SIM ou NAO:\n\n" + _transcricao(historico)
        resp = _cliente().messages.create(
            model=MODELO_RESERVA, max_tokens=5, system=_CLASSIFIER_PROMPT,
            messages=[{"role": "user", "content": conteudo}],
        )
        txt = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip().upper()
        return txt.startswith("SIM")
    except Exception:
        return False


def gerar_briefing_fechamento(historico, nome="o cliente", dados_calculadora=None):
    """Briefing de fechamento (resumo + roteiro) para quem vai fechar.
    A conversa vai como TRANSCRIÇÃO num pedido explícito, para o modelo não 'responder' a conversa."""
    import datetime as _dt
    hoje = _dt.date.today().strftime('%d/%m/%Y')
    extra = ''
    if dados_calculadora:
        extra = ("\n\nDADOS CONFIRMADOS PELA CALCULADORA/FORMULÁRIO (use estes valores exatos na seção 1):\n"
                 + _resumo_formulario(dados_calculadora) + "\n")
    conteudo = (f"DATA DE HOJE: {hoje}." + extra + "\n\n"
                f"Aqui está a conversa entre a {NOME} (atendimento) e o lead. NÃO responda a conversa: "
                "ANALISE e gere o BRIEFING DE FECHAMENTO COMPLETO, com as 5 seções.\n\n"
                "=== CONVERSA ===\n" + _transcricao(historico) + "\n=== FIM ===\n\n"
                "Gere agora o BRIEFING DE FECHAMENTO completo.")
    msgs = [{"role": "user", "content": conteudo}]
    melhor = ""
    for _ in range(2):
        resp = _cliente().messages.create(
            model=MODELO_BRIEFING, max_tokens=3000,
            system=_BRIEFING_PROMPT.replace('{nome}', nome), messages=msgs,
        )
        txt = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
        if len(txt) > len(melhor):
            melhor = txt
        if len(txt) >= 600 and 'ROTEIRO' in txt.upper():
            return txt
    return melhor
