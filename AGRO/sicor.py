"""
Dados PUBLICOS de credito rural (sem credencial), so com a biblioteca padrao do Python:

- SICOR / Banco Central (API Olinda, OData): contratos de credito rural por municipio.
  Base: https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/
- IBGE (servicodados): nome oficial dos municipios e mesorregiao.

Pegadinhas da API do SICOR (conferidas em campo):
- `cdEstado` NAO e o codigo IBGE da UF: e um codigo interno do BCB (tabela SICOR_UF abaixo).
- O filtro precisa ir com espaco codificado como %20 (quote com safe="'").
- Nao aceita $count. $skip junto com $filter volta 500 (paginacao quebrada): a busca e feita
  mes a mes (MesEmissao), com $top alto e erro se bater no limite.
- A API devolve 500 "Erro desconhecido" de vez em quando: repetir a chamada resolve.
- As linhas de CusteioMunicipioProduto sao AGREGADAS (nao sao contratos); a QUANTIDADE de
  contratos so existe em CusteioInvestimentoComercialIndustrialSemFiltros.
- nomeProduto vem entre aspas: '"SOJA"', '"BOVINOS"'.
- SICOR registra so as EMISSOES (contratos novos no ano), nao o saldo devedor nem a inadimplencia.
"""
import errno
import json
import os
import socket
import time
import urllib.error
import urllib.request
from datetime import date
from urllib.parse import quote

BASE = 'https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata'
IBGE = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios'
AGENTE = 'radar-credito-rural/1.0 (python urllib)'

# cdEstado do SICOR -> UF (codigo interno do BCB, validado por amostragem).
# AP e DF nao foram validados: ficam fora ate alguem conferir o codigo na API.
SICOR_UF = {
    '1': 'AC', '2': 'AL', '3': 'AM', '5': 'BA', '6': 'CE', '8': 'ES', '10': 'GO', '11': 'MA',
    '12': 'MG', '13': 'MS', '14': 'MT', '15': 'PA', '16': 'PB', '17': 'PE', '18': 'PI', '19': 'PR',
    '20': 'RJ', '21': 'RN', '22': 'RO', '23': 'RR', '24': 'RS', '25': 'SC', '26': 'SE', '27': 'SP',
    '28': 'TO',
}
UF_SICOR = {v: k for k, v in SICOR_UF.items()}
UFS_DISPONIVEIS = sorted(UF_SICOR)

# Ajustaveis pela CLI (radar --timeout / --tentativas)
TIMEOUT = 150
ESPERAS = (5, 15, 30, 60)   # segundos entre tentativas (o servidor do BCB oscila muito)
LIMITE = 50000              # linhas por consulta; se vier exatamente isso, o mes foi cortado


class ErroSicor(RuntimeError):
    pass


class SemConexao(ErroSicor):
    """Falha de rede (DNS, sem internet, timeout de conexao): nao adianta insistir."""


def configurar(timeout=None, tentativas=None):
    global TIMEOUT, ESPERAS
    if timeout:
        TIMEOUT = timeout
    if tentativas is not None:
        ESPERAS = (5, 15, 30, 60, 90, 120)[:max(0, tentativas - 1)]


def _baixar(url, timeout):
    req = urllib.request.Request(url, headers={'User-Agent': AGENTE, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        bruto = r.read()
    try:
        return json.loads(bruto.decode('utf-8'))
    except UnicodeDecodeError:
        return json.loads(bruto.decode('latin-1'))


def _e_falha_de_rede(e):
    """DNS, conexao recusada ou rede inalcancavel. Timeout de leitura NAO conta (o BCB e lento: repete)."""
    if isinstance(e, urllib.error.HTTPError):
        return False
    r = getattr(e, 'reason', e)
    if isinstance(r, (socket.gaierror, ConnectionRefusedError)):
        return True
    return isinstance(r, OSError) and getattr(r, 'errno', None) in (
        errno.ENETUNREACH, errno.EHOSTUNREACH, 10051, 10065)


def _get(url, timeout=None):
    timeout = timeout or TIMEOUT
    ultimo = None
    for i in range(len(ESPERAS) + 1):
        try:
            return _baixar(url, timeout)
        except urllib.error.HTTPError as e:
            ultimo = f'HTTP {e.code}'
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as e:
            ultimo = f'{type(e).__name__}: {getattr(e, "reason", e)}'
            if _e_falha_de_rede(e) and i == 0:
                # sem internet / DNS: falha na hora, sem gastar minutos repetindo
                raise SemConexao(ultimo) from None
        except ValueError as e:
            ultimo = f'resposta invalida ({e})'
        if i < len(ESPERAS):
            time.sleep(ESPERAS[i])
    raise ErroSicor(f'SICOR nao respondeu depois de {len(ESPERAS) + 1} tentativa(s) ({ultimo})')


def testar_conexao(timeout=15):
    """
    Pede o documento de servico da API Olinda (resposta leve e rapida). Levanta SemConexao/ErroSicor
    se falhar. Obs.: as consultas de dados em si sao lentas (30-60 s cada e as vezes 500): normal.
    """
    url = f'{BASE}/?$format=json'
    try:
        _baixar(url, timeout)
    except urllib.error.HTTPError as e:
        raise ErroSicor(f'HTTP {e.code}') from None
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError, ValueError) as e:
        raise SemConexao(f'{type(e).__name__}: {getattr(e, "reason", e)}') from None
    return True


def filtro(uf=None, ano=None, **iguais):
    partes = []
    if uf:
        cd = UF_SICOR.get(uf.upper())
        if not cd:
            raise ValueError(f'UF fora do mapeamento do SICOR: {uf} (disponiveis: {", ".join(UFS_DISPONIVEIS)})')
        partes.append(f"cdEstado eq '{cd}'")
    if ano:
        partes.append(f"AnoEmissao eq '{ano}'")
    for campo, valor in iguais.items():
        partes.append(f"{campo} eq '{valor}'")
    return ' and '.join(partes)


def buscar(entidade, filtro_odata='', campos=None, limite=LIMITE):
    """Uma consulta ao SICOR, sem paginacao ($skip + $filter quebra na API: ver buscar_ano)."""
    qs = ['$format=json', f'$top={limite}']
    if filtro_odata:
        qs.append('$filter=' + quote(filtro_odata, safe="'"))
    if campos:
        qs.append('$select=' + ','.join(campos))
    linhas = _get(f'{BASE}/{entidade}?' + '&'.join(qs)).get('value', [])
    if len(linhas) >= limite:
        raise ErroSicor(f'{entidade}: a consulta bateu no limite de {limite} linhas ({filtro_odata}); '
                        'dividir mais o filtro')
    return linhas


def _mes_fechado(ano, mes):
    hoje = date.today()
    return (int(ano), mes) < (hoje.year, hoje.month)


def buscar_ano(entidade, uf, ano, campos=None, aviso=None, cache=None, **iguais):
    """
    Todas as linhas de um ano, consultando MES A MES (01 a 12), um de cada vez (em paralelo o
    servidor do BCB recusa). Meses ja fechados ficam em cache para a proxima rodada nao baixar de
    novo. Devolve (linhas, meses_que_falharam). SemConexao sobe direto (nao adianta seguir).
    """
    linhas, falharam = [], []
    for mes in range(1, 13):
        arq = None
        if cache:
            extra = '_'.join(str(v).strip('"') for v in iguais.values())
            arq = os.path.join(cache, f"{entidade}_{uf}_{ano}_{mes:02d}{'_' + extra if extra else ''}.json")
            if os.path.exists(arq):
                with open(arq, encoding='utf-8') as f:
                    linhas += json.load(f)
                if aviso:
                    aviso(len(linhas))
                continue
        if (int(ano), mes) > (date.today().year, date.today().month):
            continue   # mes futuro: nada a buscar
        try:
            lote = buscar(entidade, filtro(uf, ano, MesEmissao=f'{mes:02d}', **iguais), campos)
        except SemConexao:
            raise
        except ErroSicor as e:
            falharam.append(mes)
            if len(falharam) >= 3 and len(falharam) == mes and not linhas:
                # 3 primeiros meses falharam e nada veio: servidor fora do ar, nao gastar mais tempo
                raise ErroSicor(f'{entidade}: os meses 1 a {mes} falharam em sequencia ({e})') from None
            continue
        linhas += lote
        if arq and _mes_fechado(ano, mes):
            os.makedirs(cache, exist_ok=True)
            with open(arq, 'w', encoding='utf-8') as f:
                json.dump(lote, f, ensure_ascii=False)
        if aviso:
            aviso(len(linhas))
    return linhas, falharam


def totais_municipio(uf, ano, aviso=None, cache=None):
    """Quantidade e valor de custeio/investimento por municipio (com atividade agricola/pecuaria)."""
    campos = ['codMunicIbge', 'cdMunicipio', 'Municipio', 'Atividade', 'QtdCusteio', 'VlCusteio',
              'QtdInvestimento', 'VlInvestimento', 'AreaCusteio', 'AreaInvestimento']
    return buscar_ano('CusteioInvestimentoComercialIndustrialSemFiltros', uf, ano, campos, aviso, cache)


def custeio_por_produto(uf, ano, produto, aviso=None, cache=None):
    """Valor e area de custeio de um produto (ex.: SOJA, BOVINOS) por municipio."""
    campos = ['codIbge', 'Municipio', 'VlCusteio', 'AreaCusteio']
    return buscar_ano('CusteioMunicipioProduto', uf, ano, campos, aviso, cache, nomeProduto=f'"{produto}"')


def municipios_ibge(uf, timeout=60):
    """{codigo_ibge: {'nome', 'mesorregiao'}} dos municipios da UF (API publica do IBGE)."""
    dados = _baixar(IBGE.format(uf=uf.upper()), timeout)
    saida = {}
    for m in dados:
        meso = ''
        micro = m.get('microrregiao') or {}
        if micro.get('mesorregiao'):
            meso = micro['mesorregiao'].get('nome', '')
        elif m.get('regiao-imediata'):
            inter = m['regiao-imediata'].get('regiao-intermediaria') or {}
            meso = inter.get('nome', '')
        saida[str(m['id'])] = {'nome': m['nome'], 'mesorregiao': meso}
    return saida
