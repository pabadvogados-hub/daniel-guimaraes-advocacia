# -*- coding: utf-8 -*-
"""
Cobranca automatica de ENVIO DE DOCUMENTOS (pos-assinatura) - Daniel Guimarães Advocacia.

Diferente da cobranca de assinatura, aqui NAO ha "assinou" no ZapSign como
trava. O cliente manda os documentos e a EQUIPE encerra manualmente quando
recebe tudo (--recebido). Cadencia mais gentil (a cada 2 dias), pois juntar
documento leva tempo.

Braco de envio = D-API (numero oficial, via wa_dapi.py) desde 24/09/2026.

Comandos:
  Inscrever (checklist da analise inicial do produtor rural):
    python cobranca_documentos.py --enroll --nome "Fulano de Tal" --tel "00900000000"
  Processar a fila (simulacao, padrao):
    python cobranca_documentos.py
  Processar de verdade:
    python cobranca_documentos.py --enviar
  Encerrar quando recebeu os documentos:
    python cobranca_documentos.py --recebido --nome "Fulano de Tal"
  Ver a fila:
    python cobranca_documentos.py --status
"""
import os, sys, io, json
from datetime import datetime, timezone

try:
    # so reembrulha se preciso: reembrulhar stdout ja-utf8 FECHA o buffer
    # compartilhado e derruba quem importou este modulo (crash de 12/08).
    if (getattr(sys.stdout, "encoding", "") or "").lower().replace("-", "") != "utf8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_RAIZ, "INTEGRACOES"))
from dotenv import load_dotenv
load_dotenv(os.getenv(
    "ESC_CONFIG_ENV",
    r"C:\AUTOMAÇÕES\AUTOMACOES_PROJETO_COMPLETO_2026-07-19\config\.env"))
if os.path.exists("/opt/escritorio/config/.env"):
    load_dotenv("/opt/escritorio/config/.env")

import requests

# Envio pela D-API (numero oficial do escritorio) via wa_dapi.py, desde 24/09/2026:
# a Z-API desconectou em 23/09 ~14:30 e seguia devolvendo 200 sem entregar.
# Regra vigente (Advogada, 10/08/2026): NAO enviar pelo Atende Direito/ADONE - responde
# ok e NAO entrega.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # wa_dapi mora em SYNC/
import wa_dapi


def _ddi(tel):
    d = "".join(ch for ch in str(tel) if ch.isdigit())
    return d if d.startswith("55") else "55" + d


def zapi_enviar_texto(telefone, texto):
    """Nome antigo mantido; o envio sai pela D-API (wa_dapi). True so com envio aceito."""
    try:
        ok, info = wa_dapi.enviar_texto(_ddi(telefone), texto)
        if not ok:
            print(f"  (d-api recusou: {str(info)[:160]})")
        return bool(ok)
    except Exception as e:
        print(f"  (d-api erro: {str(e)[:120]})")
        return False


def _dapi_configurado():
    try:
        wa_dapi._cred()
        return True
    except Exception:
        return False

ENVIAR = "--enviar" in sys.argv
INTERVALO = 2      # dias entre mensagens (cadencia gentil)
MAX_TOQUES = 5     # apos isso, para e alerta o time
FILA = os.path.join(os.path.dirname(__file__), "cobranca_documentos_fila.json")

FIG_TIPO = "sticker"
FIGURINHAS = {1: "", 2: "", 3: "", 4: "", 5: ""}

# Checklist do PRODUTOR RURAL (defesa contra bancos). Editavel por cliente no enroll (--checklist).
#
# DUAS FASES:
#   CHECKLIST_PADRAO (= OBRIGATORIOS PARA A ANALISE INICIAL): e o que a cobranca automatica pede
#     depois da assinatura. Sem isso o advogado nao consegue ver a divida, o contrato e a garantia.
#   CHECKLIST_DEPOIS (FASE SEGUINTE): documentos do imovel e da producao que a equipe pede quando o
#     caminho estiver definido (pedido de prorrogacao, defesa na execucao, revisional). NAO entram na
#     cobranca automatica: muitos saem de cartorio/orgao publico e levam dias.
#
# REGRA DA EQUIPE (herdada da base): extrato da CONTA CORRENTE nao entra na cobranca automatica
# (cliente teme golpe quando o WhatsApp pede extrato). O que se pede aqui e o DEMONSTRATIVO DA
# DIVIDA, que o banco fornece na agencia.
#
# O papel judicial (citacao, mandado, edital de leilao) NAO entra no padrao: so com sinal de
# cobranca judicial no caso (ver `_tem_cobranca_judicial`). Cobrar documento que nao existe
# queima a confianca do cliente.
ITEM_BO = "Foto da citacao, mandado ou edital de leilao que voce recebeu"   # nome mantido: item de excecao
CHECKLIST_PADRAO = [
    "Documento com foto (RG ou CNH) e CPF; se for casado(a), tambem os do conjuge",
    "Comprovante de endereco",
    "Cedulas e contratos do banco (custeio, investimento, Pronaf, CPR, CCB): foto de todas as paginas",
    "Demonstrativo ou planilha da evolucao da divida (pedir na agencia do banco)",
    "Cartas, notificacoes e mensagens do banco sobre a divida",
    "Prova da perda da safra que tiver: laudo, Proagro, seguro rural ou decreto de emergencia do municipio",
]
CHECKLIST_DEPOIS = [
    "Matricula atualizada do imovel rural",
    "CCIR (Certificado de Cadastro de Imovel Rural)",
    "ITR dos ultimos anos",
    "CAR (Cadastro Ambiental Rural)",
    "DAP ou CAF (se a operacao for Pronaf)",
    "Notas fiscais de produtor ou talao (safra boa e safra ruim)",
    "Orcamento ou projeto tecnico do financiamento",
]
# E-MAIL NAO E COBRADO (Advogada, 24/09/2026, reforcado em 25/09): estado civil e
# e-mail nao sao obrigatorios; saem da ligacao de fechamento quando houver.
_NAO_COBRAR = r"e-?mail"


def arg(flag, default=None):
    if flag in sys.argv:
        i = sys.argv.index(flag)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


# ------------------------------------------------------------------ mensagens
def _checklist_txt(checklist):
    return "\n".join(f"- {item}" for item in checklist)


def ja_chegou(nome):
    """Tipos que a varredura de provas ja classificou na pasta deste cliente."""
    try:
        with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "varredura_provas_state.json"), encoding="utf-8") as f:
            st = (json.load(f).get("clientes") or {}).get(nome) or {}
    except Exception:
        return []
    # audio nao e documento: entra na pasta, mas nao se agradece como prova
    return [t for t in (st.get("tipos") or {}) if t != "audio"]


def msg(toque, nome, checklist, recebidos=None):
    p = (nome or "").split()[0].title() if nome else "amigo(a)"
    # EXTRATO BANCARIO NUNCA VAI PARA O CLIENTE (Advogada, 26/10/2026): "as vezes assusta
    # eles". Sai de qualquer texto daqui, inclusive dos cinco toques antigos; quem pede
    # e a Advogada, pela tarefa que a varredura abre quando o card anda.
    try:
        import varredura_provas as _vp
        checklist = [i for i in (checklist or []) if not _vp.RX_SO_RESPONSAVEL.search(i)]
    except Exception:
        pass
    # PEDIDO VAZIO NUNCA (Advogada, 26/10/2026): quem ja mandou alguma coisa ouve primeiro o
    # que chegou, e so entao o que falta. O texto e o MESMO do aceite da varredura, para
    # nao existirem duas versoes da mesma fala.
    chegou = ja_chegou(nome) if recebidos is None else list(recebidos)
    if chegou:
        try:
            import varredura_provas as _vp
            t = _vp.texto_aceite(nome, chegou, checklist, False, toque)
            if t:
                return t
        except Exception as e:
            print(f"  (aceite indisponivel, segue o texto padrao: {str(e)[:90]})")
    if toque == 1:
        return (f"{p}, agora que esta tudo assinado, vamos comecar a cuidar da sua divida com o banco.\n\n"
                f"Assim que voce mandar os documentos, o advogado analisa os contratos e a situacao da "
                f"cobranca e define o melhor caminho. Quanto antes chegar, antes a gente age.\n\n"
                f"Separei a lista (pode mandar foto pelo celular mesmo):\n\n"
                + _checklist_txt(checklist) +
                f"\n\nMe manda o que voce ja tiver AINDA HOJE, que o resto a gente vai completando. "
                f"Qualquer duvida de onde achar, e so chamar aqui.\nDaniel Guimarães Advocacia")
    if toque == 2:
        return (f"Ola, {p}. Para a analise do seu caso comecar, falta so os documentos.\n\n"
                f"Se conseguir priorizar UM, mande o primeiro da sua lista: *{(checklist[0] if checklist else 'o que voce ja tiver')}*. "
                f"Consegue mandar ainda hoje?\n\n"
                f"Pode ser foto ou print, do jeito que for mais rapido para voce.\nDaniel Guimarães Advocacia")
    if toque == 3:
        return (f"{p}, tudo certo? Em divida rural cada dia conta: prazo do banco, da execucao e do "
                f"leilao corre sem esperar.\n\n"
                f"Nao precisa ser nada formatado, foto pelo celular resolve. Se nao tiver a copia das "
                f"cedulas, pode pedir na agencia que eles sao obrigados a fornecer.\n\n"
                f"Ficou com duvida em algum? Me fala que eu explico na hora.\nDaniel Guimarães Advocacia")
    if toque == 4:
        return (f"Ola, {p}. Vamos destravar isso juntos?\n\n"
                f"Se algum documento da lista estiver dificil de achar, me diz qual que eu explico "
                f"onde pegar, passo a passo. Manda o que ja tiver hoje e o resto a gente "
                f"resolve junto.\nDaniel Guimarães Advocacia")
    return (f"{p}, o seu caso esta so esperando os documentos, e eu nao quero te deixar "
            f"perdendo tempo. Vou pedir para uma pessoa da equipe te ligar e ajudar "
            f"a reunir tudo rapido.\nDaniel Guimarães Advocacia")


# ------------------------------------------------------------------ fila
def carregar():
    if os.path.exists(FILA):
        try:
            with open(FILA, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"clientes": {}}


def salvar(f):
    with open(FILA, "w", encoding="utf-8") as fp:
        json.dump(f, fp, ensure_ascii=False, indent=2)


# ------------------------------------------------------------------ enroll / recebido
def _tem_cobranca_judicial(cid, nome="", tel=""):
    """So pede a citacao/mandado/edital quando o caso tem cobranca judicial de verdade.

    Olha, nesta ordem: o campo `situacao` da ficha de entrevista (execucao, leilao, busca e
    apreensao, consolidacao) e, depois, as notas da conversa.
    Na duvida devolve False: e melhor deixar de pedir um documento que existe do
    que cobrar cinco vezes um documento que nunca existiu.
    """
    import re as _re
    import sqlite3 as _sq
    if not cid:
        return False
    palavras = _re.compile(r"execu[cç][aã]o|executad|leil[aã]o|edital|cita[cç][aã]o|citad|mandado|"
                           r"busca e apreens|apreendid|oficial de justi[cç]a|consolida[cç][aã]o", _re.I)
    try:
        con = _sq.connect("/opt/escritorio/SISTEMA/backend/sistema_esc.db", timeout=15)
        r = con.execute("select valor from ficha_entrevista where conversa_id=? and campo='situacao'",
                        (cid,)).fetchone()
        if r and palavras.search(r[0] or ""):
            con.close()
            return True
        n = con.execute("select notas from wa_conversas where id=?", (cid,)).fetchone()
        con.close()
        return bool(n and n[0] and palavras.search(n[0]))
    except Exception:
        return False

def enroll_cliente(nome, tel="", checklist=None, cid=None, podar=True):
    """Inscreve o cliente na cobranca de documentos.

    Quando o chamador nao informa `checklist`, o padrao e PODADO pela
    transcricao da reuniao de fechamento (`checklist_documentos.montar`), para
    nao cobrar documento que o cliente ja disse que nao existe (licao herdada da base:
    pedir cinco vezes um papel que nao existe queima a confianca). A poda so remove
    item que a transcricao contradiz EXPRESSAMENTE e, em qualquer falha, mantem
    o checklist padrao - nunca fica pior que antes.
    """
    itens = list(checklist) if checklist else None
    origem = "informado pelo chamador" if checklist else None
    # papel judicial nao vem no padrao: entra so se o caso tiver cobranca judicial
    bo_cabe = _tem_cobranca_judicial(cid, nome, tel)
    if itens is None and podar:
        try:
            from checklist_documentos import montar
            itens, origem = montar(nome, tel, list(CHECKLIST_PADRAO), cid=cid)
            if not itens:
                origem = "pendente: " + (origem or "?")
        except Exception as e:
            origem = f"pendente: erro {str(e)[:80]}"
    elif itens is None:
        itens, origem = list(CHECKLIST_PADRAO), "padrao (poda desligada)"
    # O papel judicial e o unico item que entra por excecao, nunca por padrao: so quando a
    # ficha ou a conversa mostram execucao, leilao ou busca e apreensao. Vai em PRIMEIRO
    # lugar porque define o prazo.
    if bo_cabe and itens is not None and ITEM_BO not in itens:
        itens = [ITEM_BO] + list(itens)
        origem = (origem or "") + " + papel judicial (caso tem cobranca judicial)"
    fila = carregar()
    fila["clientes"][nome] = {
        "nome": nome,
        "telefone": tel or "",
        "checklist": itens,
        "checklist_origem": origem,
        "data_inicio": str(datetime.now(timezone.utc).date()),
        "ultimo_envio": None,
        "toques": 0,
        "encerrado": False,
    }
    salvar(fila)
    print(f"[docs] inscrito: {nome} | tel {tel} | "
          + (f"{len(itens)} itens ({origem})" if itens else f"SEM LISTA ({origem})"))
    return True


def enroll():
    nome = arg("--nome")
    if not nome:
        print("Uso: --enroll --nome \"Nome Completo\" [--tel \"19999999999\"]")
        return
    enroll_cliente(nome, arg("--tel") or "")


def recebido():
    nome = arg("--nome")
    fila = carregar()
    c = fila["clientes"].get(nome)
    if not c:
        print(f"'{nome}' nao esta na fila de documentos.")
        return
    c["encerrado"] = True
    salvar(fila)
    print(f"[docs] ENCERRADO: {nome} (documentos recebidos). Nao sera mais cobrado.")


def status():
    fila = carregar()
    if not fila["clientes"]:
        print("Fila vazia.")
        return
    for nome, c in fila["clientes"].items():
        flag = "ENCERRADO" if c.get("encerrado") else "ativo"
        print(f"- {nome} | tel {c.get('telefone')} | inicio {c.get('data_inicio')} "
              f"| ultimo {c.get('ultimo_envio')} | toques {c.get('toques')} | {flag}")


# ------------------------------------------------------------------ processar
def _inicial_pronta(tel):
    """True se o card do cliente ja esta na Producao em Revisao, Distribuicao ou Distribuida."""
    import sqlite3 as _sq
    d = "".join(ch for ch in str(tel or "") if ch.isdigit())[-8:]
    if len(d) < 8:
        return False
    try:
        con = _sq.connect("file:/opt/escritorio/SISTEMA/backend/sistema_esc.db?mode=ro", uri=True, timeout=15)
        r = con.execute("select etapa from wa_conversas where numero_id=1 and pipeline_id=18 and "
                        "contato_telefone like ? order by atualizado_em desc limit 1", ("%" + d,)).fetchone()
        con.close()
        return bool(r and r[0] in ("Revisao", "Distribuicao", "Distribuida"))
    except Exception:
        return False


def processar():
    hoje = datetime.now(timezone.utc).date()
    modo = "ENVIAR (producao)" if ENVIAR else "DRY-RUN (simulacao)"
    print(f"=== COBRANCA DE DOCUMENTOS | {hoje} | {modo} ===\n")
    if ENVIAR and not _dapi_configurado():
        print("Sem credencial de envio (D-API: wa_numeros id 1 / DAPI_SESSION+DAPI_TOKEN) - nada enviado.")
        return

    fila = carregar()
    if not fila["clientes"]:
        print("Fila vazia. Inscreva com --enroll.")
        return

    for nome, c in fila["clientes"].items():
        if c.get("encerrado"):
            print(f"[{nome}] encerrado. skip.")
            continue

        # INICIAL JA PRONTA (Titular, 29/09/2026: "o cliente A pode parar de cobrar, ja
        # finalizamos a inicial dele"): card na Producao em Revisao, Distribuicao ou Distribuida
        # = documento nao faz mais falta. Encerra e nao manda nada.
        if _inicial_pronta(c.get("telefone")):
            c["encerrado"] = True
            print(f"[{nome}] inicial ja pronta (card em Revisao ou depois). cobranca encerrada.")
            continue

        # LISTA DO CASO (Advogada, 11/09/2026): sem lista confiavel NAO cobra as
        # cegas; reanalisa a cada rodada e avisa o time enquanto pender.
        if not _garantir_checklist(nome, c):
            continue

        # O QUE O CLIENTE JA DISSE QUE NAO TEM SAI DA LISTA: se ele escreveu "nao tenho laudo"
        # ou "nunca recebi carta do banco", a cobranca para de pedir esses itens.
        _podar_pelo_que_o_cliente_disse(nome, c)
        if not c.get("checklist"):
            c["encerrado"] = True
            print(f"[{nome}] lista zerada pelo que o cliente escreveu; cobranca encerrada.")
            # mandou o que tinha e disse que nao tem o resto: vai direto para a
            # producao da inicial, sem esperar a varredura do dia seguinte (Advogada, 25/09)
            try:
                import varredura_provas as _vp
                cid = _vp.conversa_por_tel(c.get("telefone"))
                if cid:
                    _vp.mover_para_producao(cid, ENVIAR, quem="auto:cobranca-documentos",
                                            origem="script:cobranca_documentos")
                    if ENVIAR:
                        zapi_enviar_texto(TEL_TIME,
                            f"📁 {nome}: mandou o que tinha e disse que não tem o resto. "
                            f"Card movido para Produção > Produção da Inicial.")
            except Exception as e:
                print(f"[{nome}] aviso: nao movi para a producao: {str(e)[:120]}")
            continue

        # JA MANDOU: pausa e confere, em vez de insistir
        if c.get("pausa_ja_mandou"):
            print(f"[{nome}] pausado desde {c['pausa_ja_mandou']}: cliente disse que ja mandou "
                  "(conferencia humana). skip.")
            # pausa nao pode virar parada esquecida: relembra a Dra. Advogada a cada 3 dias
            ult = c.get("pausa_alertada") or c["pausa_ja_mandou"]
            if ENVIAR and (hoje - datetime.fromisoformat(ult).date()).days >= 3:
                zapi_enviar_texto(TEL_TIME,
                    f"📂 {nome}: a cobrança segue pausada desde {c['pausa_ja_mandou']} (ele disse "
                    f"que já mandou). Falta conferir a pasta e mover o card, ou pedir para "
                    f"retomar a cobrança.")
                c["pausa_alertada"] = str(hoje)
            continue
        prova = _disse_que_ja_mandou(c.get("telefone"), c.get("ultimo_envio") or c.get("data_inicio"))
        if prova:
            c["pausa_ja_mandou"] = str(hoje)
            print(f"[{nome}] PAUSADO: cliente disse que ja mandou | \"{prova[:120]}\"")
            if ENVIAR:
                zapi_enviar_texto(TEL_TIME,
                    f"📂 {nome} disse que já mandou os documentos (\"{prova[:100]}\"). Parei a "
                    f"cobrança dele para não insistir. Pela lista ainda falta: "
                    f"{'; '.join(c.get('checklist') or [])}. Conferir a pasta (o que a visão não "
                    f"reconheceu fica como OUTRO_) e, se estiver completo, mover o card para "
                    f"Produção da Inicial.")
            continue

        # respeita a cadencia (a cada INTERVALO dias)
        if c.get("ultimo_envio"):
            try:
                ult = datetime.fromisoformat(c["ultimo_envio"]).date()
                if (hoje - ult).days < INTERVALO:
                    print(f"[{nome}] dentro do intervalo ({INTERVALO}d). skip.")
                    continue
            except Exception:
                pass

        toque = int(c.get("toques", 0)) + 1
        if toque > MAX_TOQUES:
            print(f"[{nome}] >> toque {toque}: PARANDO. ALERTA INTERNO: cobrar documentos manualmente.")
            c["encerrado"] = True
            continue

        enviado = _disparar(nome, c["telefone"], msg(toque, c["nome"], c["checklist"]), toque)
        if enviado:
            c["ultimo_envio"] = str(hoje)
            c["toques"] = toque

    salvar(fila)
    print("\n=== fim ===")


TEL_TIME = os.getenv("TEL_ALERTA_EQUIPE", "")

# item do checklist -> como o cliente se refere a ele
_ITEM_PALAVRA = [
    (r"laudo|proagro|perda da safra", r"laudo|proagro|seguro|decreto|emerg[eê]ncia"),
    (r"cartas|notifica", r"carta|notifica[cç]"),
    (r"conjuge", r"c[oô]njuge|esposa|marido|mulher"),
    (r"demonstrativo|planilha", r"demonstrativo|planilha|evolu[cç][aã]o"),
    (r"e-?mail", r"e-?mail"),
]
_NEGA = (r"n[aã]o\s+(tenho|tinha|tem|tive|recebi|recebia|davam|dava|existe|existia|"
         r"vai\s+querer|v[aã]o\s+querer|quer(em)?|conhe[cç]o)|nunca\s+(tive|recebi|me\s+deram)|"
         r"ningu[eé]m\s+(vai|quer)|n[aã]o\s+me\s+davam|"
         r"n[aã]o\s+me\s+(deram|deu(?!\s+tempo)|entregaram|entregou|passaram|passou|mandaram)|"
         r"n[aã]o\s+(deram|entregaram)")

# Cliente que diz que ja mandou ("eu ja mandei", "mandei varias coisas") nao leva mais
# lembrete: a cobranca
# pausa e a Dra. Advogada confere a pasta (o que a visao nao reconheceu fica como OUTRO_).
_JA_MANDEI = (r"j[aá]\s+(te\s+|lhe\s+|os\s+|as\s+)?(mandei|enviei|encaminhei|passei)|"
              r"(mandei|enviei)\s+(tudo|v[aá]rias|v[aá]rios)")


def _disse_que_ja_mandou(tel, desde):
    """Texto do cliente, a partir do dia do ultimo lembrete, dizendo que ja mandou."""
    import sqlite3 as _sq
    import re as _re
    t8 = "".join(ch for ch in (tel or "") if ch.isdigit())[-8:]
    if not t8 or not desde:
        return None
    try:
        con = _sq.connect("file:/opt/escritorio/SISTEMA/backend/sistema_esc.db?mode=ro",
                          uri=True, timeout=15)
        cids = [r[0] for r in con.execute("select id, contato_telefone from wa_conversas")
                if "".join(ch for ch in (r[1] or "") if ch.isdigit())[-8:] == t8]
        textos = []
        for cid in cids:
            textos += [r[0] for r in con.execute(
                "select conteudo from wa_mensagens where conversa_id=? and origem='contato' "
                "and tipo in ('texto','audio') and criado_em>=? and coalesce(conteudo,'')<>''",
                (cid, str(desde)))]
        con.close()
    except Exception:
        return None
    return next((t for t in textos if _re.search(_JA_MANDEI, t, _re.I)), None)


def _textos_do_cliente(tel):
    """Textos e audios transcritos que o cliente mandou (conversa pelo telefone)."""
    import sqlite3 as _sq
    t8 = "".join(ch for ch in (tel or "") if ch.isdigit())[-8:]
    if not t8:
        return []
    try:
        con = _sq.connect("file:/opt/escritorio/SISTEMA/backend/sistema_esc.db?mode=ro",
                          uri=True, timeout=15)
        cids = [r[0] for r in con.execute("select id, contato_telefone from wa_conversas")
                if "".join(ch for ch in (r[1] or "") if ch.isdigit())[-8:] == t8]
        out = []
        for cid in cids:
            out += [r[0] for r in con.execute(
                "select conteudo from wa_mensagens where conversa_id=? and origem='contato' "
                "and tipo in ('texto','audio') and coalesce(conteudo,'')<>''", (cid,))]
        con.close()
        return out
    except Exception:
        return []


def _podar_pelo_que_o_cliente_disse(nome, c):
    import re as _re
    itens = [i for i in (c.get("checklist") or []) if not _re.search(_NAO_COBRAR, i, _re.I)]
    if len(itens) != len(c.get("checklist") or []):
        print(f"[{nome}] e-mail tirado da lista (nao e obrigatorio).")
        c["checklist"] = itens
    if not itens:
        return
    textos = _textos_do_cliente(c.get("telefone"))
    tirados = []
    for item in itens:
        for rx_item, rx_palavra in _ITEM_PALAVRA:
            if not _re.search(rx_item, item, _re.I):
                continue
            prova = next((t for t in textos if _re.search(rx_palavra, t, _re.I)
                          and _re.search(_NEGA, t, _re.I)), None)
            if prova:
                tirados.append((item, prova))
            break
    if not tirados:
        return
    c["checklist"] = [i for i in itens if i not in {x for x, _ in tirados}]
    c.setdefault("podados_pelo_cliente", []).extend(x for x, _ in tirados)
    for item, prova in tirados:
        print(f"[{nome}] REMOVIDO pelo que o cliente escreveu: {item} | \"{prova[:120]}\"")
    if ENVIAR:
        zapi_enviar_texto(TEL_TIME,
            f"📝 {nome}: tirei da cobranca o que o cliente disse que nao tem: "
            + "; ".join(f"{i} (\"{p[:80]}\")" for i, p in tirados)
            + ". Se precisar de prova substituta, combinar com ele pessoalmente.")


def _garantir_checklist(nome, c):
    """True = pode cobrar; False = segura este cliente nesta rodada.

    Regra da Advogada (11/09/2026, caso a equipe): a lista padrao e do caso COMUM;
    cliente sem analise do caso nao recebe cobranca as cegas. Reanalisa a
    cada rodada (transcricao OU ficha); cliente antigo ja em cobranca segue
    com a lista atual, mas tambem e reanalisado e o time e avisado.
    """
    origem = c.get("checklist_origem") or ""
    if c.get("checklist") and origem and not origem.startswith(("pendente", "padrao")):
        return True
    try:
        from checklist_documentos import montar
        itens, motivo = montar(nome, c.get("telefone") or "", list(CHECKLIST_PADRAO))
    except Exception as e:
        itens, motivo = None, f"erro {str(e)[:80]}"
    if itens:
        antes = len(c.get("checklist") or [])
        c["checklist"], c["checklist_origem"] = itens, motivo
        print(f"[{nome}] lista do caso pronta: {antes or 'sem'} -> {len(itens)} itens ({motivo})")
        return True
    # sem relato do caso NAO se cobra, nem quem ja vinha sendo cobrado: foi
    # exatamente assim que uma cliente gestante levou a lista comum
    _alertar_pendencia(nome, c, motivo, False)
    return False


def _alertar_pendencia(nome, c, motivo, ja_cobrando):
    hoje = datetime.now(timezone.utc).date()
    try:
        recente = c.get("alerta_pendencia") and \
            (hoje - datetime.fromisoformat(c["alerta_pendencia"]).date()).days < 3
    except Exception:
        recente = False
    rotulo = "SEGUREI a cobranca (nada enviado)"
    print(f"[{nome}] sem lista do caso ({motivo}); {rotulo}")
    if ENVIAR and not recente:
        ok = zapi_enviar_texto(TEL_TIME,
            f"⚠️ Cobranca de documentos: nao consegui montar a lista do caso "
            f"de *{nome}* ({motivo}). {rotulo}. Suba a transcricao da reuniao "
            f"(ou cole o link na ficha do card no CRM) que eu monto a lista "
            f"certa e sigo sozinho.")
        if ok:
            c["alerta_pendencia"] = str(hoje)


def _disparar(nome, telefone, texto, toque):
    fig = FIGURINHAS.get(toque, "")
    print(f"\n[{nome}] toque {toque} | tel: {telefone or 'SEM TELEFONE'}")
    print("  " + texto.replace("\n", "\n  "))
    if not ENVIAR:
        print("  (dry-run: nao enviado)")
        return False
    if not telefone:
        print("  ERRO: sem telefone")
        return False
    ok = zapi_enviar_texto(telefone, texto)
    print("  ENVIADO! (D-API)" if ok else "  ERRO no envio (D-API)")
    return ok


if __name__ == "__main__":
    if "--enroll" in sys.argv:
        enroll()
    elif "--recebido" in sys.argv:
        recebido()
    elif "--status" in sys.argv:
        status()
    else:
        processar()
