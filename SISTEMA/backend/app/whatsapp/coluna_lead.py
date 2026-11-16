# -*- coding: utf-8 -*-
"""Em qual coluna a SDR larga o lead que ela acabou de qualificar.

Regra: qualificou e viu requisitos -> Lead Qualificado ou Lead Quente conforme a temperatura;
nao identificou do que se trata -> fica na entrada para gente olhar.

Traducao para as colunas do quadro de Produtores Rurais:
  quentissimo, quente  -> Lead Quente
  morno, frio          -> Lead Qualificado
  sem caso / sem resposta -> nao move (fica na Caixa de Entrada para gente olhar)

A temperatura vem do termometro (`lead_termometro`) quando ele ja passou por ali.
Lead novo ainda nao tem temperatura, entao quem decide e o proprio papo:
- divida JA EM COBRANCA (vencida, negativada, execucao, leilao, busca e apreensao) -> Lead Quente;
- sinal de URGENCIA (leilao marcado, citacao, mandado, oficial de justica, apreensao, penhora,
  bloqueio de conta, consolidacao da propriedade) -> Lead Quente, mesmo sem o resto da qualificacao;
- divida em dia / a vencer -> Lead Qualificado.

Os nomes `saiu_no_papo` e `caso_urgente_no_papo` vieram da base (eram "ja saiu da empresa?") e foram
mantidos porque o atendimento e o painel comercial chamam por eles. Aqui "saiu" = a divida ja
saiu do normal e esta em cobranca. O backend nao importa nada do SYNC.
"""
import re
import unicodedata

from sqlalchemy import text

QUENTE = 'Lead Quente'
QUALIFICADO = 'Lead Qualificado'

POR_TEMPERATURA = {'quentissimo': QUENTE, 'quente': QUENTE,
                   'morno': QUALIFICADO, 'frio': QUALIFICADO,
                   'sem_caso': None, 'sem_resposta': None}

# "nao venceu", "ainda nao venceu", "to em dia": a divida NAO esta em cobranca
NEGOU = re.compile(r'(nao venceu|ainda nao venceu|nao esta vencid|nao ta vencid|nunca atrasei|'
                   r'nao tem execucao|nao tem leilao|nao entraram na justica|nao entrou na justica)')
SAIU = re.compile(r'(venceu|vencid|atrasad|atrasei|em atraso|nao consegui pagar|nao paguei|deixei de pagar|'
                  r'negativad|nome sujo|serasa|spc|protest|cobranca judicial|entrou na justica|'
                  r'entraram na justica|me processou|me executando|execucao|executad|leilao|leiloar|'
                  r'busca e apreensao|apreend|tomaram|vao tomar|consolidac|penhor(a|aram)|bloque(io|aram))')
FICOU = re.compile(r'(to em dia|estou em dia|esta em dia|ta em dia|pago em dia|vence (so )?(em|no|na|mes|ano)|'
                   r'vai vencer|ainda vai vencer|a vencer|antes de vencer|ainda nao venceu)')


def sa(s) -> str:
    """minuscula e sem acento."""
    return ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower())
                   if unicodedata.category(c) != 'Mn')


def saiu_no_papo(historico) -> bool:
    """Alguma fala do PRODUTOR diz que a divida ja esta em cobranca (vencida, negativada,
    execucao, leilao, busca e apreensao). Nome mantido por compatibilidade."""
    for m in (historico or []):
        if (m.get('role') or '') != 'user':
            continue
        t = ' '.join(sa(m.get('content') or '').split())
        if not t:
            continue
        if SAIU.search(t) and not (NEGOU.search(t) or FICOU.search(t)):
            return True
        if URGENTE_NA_EMPRESA.search(t):
            return True
    return False


# Urgencia real (ligar ja): ato judicial ou extrajudicial com prazo curto correndo.
URGENTE_NA_EMPRESA = re.compile(r'(leilao (marcado|dia|para|esta|ta|vai ser|d[ao] )|marc\w* (o )?leilao|edital|data do leilao|'
                                r'citad|citacao|mandado|oficial de justica|intimad|'
                                r'busca e apreensao|apreend|vieram buscar|levaram (o|a|meu|minha)|'
                                r'penhor(a|aram|ou)|bloque(io|aram|ou) (da|de|na|minha)|conta bloquead|'
                                r'consolidac|consolidar a propriedade|embargos|prazo de \d+ dias)')


def caso_urgente_no_papo(historico) -> bool:
    """Leilao marcado, citacao em execucao, busca e apreensao, penhora ou bloqueio: urgente (ligar ja)."""
    for m in (historico or []):
        if (m.get('role') or '') == 'user' and URGENTE_NA_EMPRESA.search(' '.join(sa(m.get('content') or '').split())):
            return True
    return False


async def escolher(db, conv, historico=None):
    """Coluna do quadro de Produtores Rurais para este lead, ou None quando e melhor deixar na entrada."""
    try:
        r = (await db.execute(text('select temperatura from lead_termometro where conversa_id=:c'),
                              {'c': conv.id})).first()
    except Exception:
        r = None
    if r and r[0]:
        temp = str(r[0]).strip().lower()
        if temp in POR_TEMPERATURA:
            return POR_TEMPERATURA[temp]
    return QUENTE if (saiu_no_papo(historico) or caso_urgente_no_papo(historico)) else QUALIFICADO
