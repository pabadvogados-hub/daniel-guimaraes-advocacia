# AGRO - ferramentas de captação do produtor rural

Daniel Guimarães Advocacia - defesa do produtor rural contra bancos (prorrogação/alongamento de
crédito rural, execução de cédula, leilão, busca e apreensão, revisional).

Só Python 3 (biblioteca padrão; nada para instalar). Roda de qualquer pasta:

```
python AGRO/main.py <comando>          (a partir da raiz do projeto)
cd AGRO && python main.py <comando>    (de dentro da pasta)
```

Todas as saídas vão para `AGRO/saida/` (fora do git).

## 1. Calculadora do crédito rural (juros + prorrogação)

```
python main.py calculadora
```
Gera `saida/calculadora/index.html`: página interativa, um arquivo só, sem internet. O produtor
digita valor, taxa, parcelas, carência e vê parcela, total de juros, custo efetivo anual e quanto a
parcela cai com X anos a mais de prazo. Pode ir para o site ou ser mandada como arquivo.

```
python main.py calculadora --valor "850.000,00" --taxa 12,5 --parcelas 5 --carencia 12 \
    --prorrogar-anos 3 --lead "Nome do lead" --banco "Banco X"
```
Além da página, gera a simulação pronta de um lead:
- `saida/calculadora/simulacao_<lead>_<data>.html` - relatório para enviar ao lead
- `saida/calculadora/simulacao_<lead>_<data>.txt` - resumo para colar no WhatsApp

Opções: `--taxa-tipo aa|am`, `--periodicidade anual|semestral|mensal`, `--sistema price|sac`,
`--carencia-juros pagos|capitalizados`, `--custos`, `--taxa-comparacao`, `--prorrogar-carencia`,
`--whatsapp 55DDDNUMERO` (botão da página). Ver `python main.py calculadora --help`.

PNG: não é gerado (a ferramenta de origem também não gerava). Para imagem ou PDF, abrir o HTML no
navegador e usar "Imprimir > Salvar como PDF" ou print de tela.

## 2. Radar do crédito rural (SICOR / Banco Central)

```
python main.py radar --uf GO                       (uma UF, ano anterior)
python main.py radar --uf GO,MT,MS --ano 2025
python main.py radar --uf GO --municipio "Cidade A,Cidade B"
python main.py radar --uf TODAS                    (Brasil inteiro: demora bastante)
```
Dados públicos da API Olinda do Banco Central (SICOR) + IBGE. Gera CSV, HTML e JSON em
`saida/radar/` com: ranking de municípios por índice (contratos + valor financiado + custeio dos
produtos de foco), ranking de regiões (mesorregiões do IBGE) e a lista sugerida para anúncio e
prospecção. `--uf` é obrigatório (não há UF padrão).

- A API do BCB é lenta (30-60 s por consulta) e às vezes devolve erro 500: cada UF faz 12
  consultas (uma por mês) + 12 por produto de foco. Meses já baixados ficam em
  `saida/radar/cache/`; se faltar algum, rode o mesmo comando de novo.
- `--produtos SOJA,MILHO,BOVINOS` troca os produtos de foco (`--produtos ""` = nenhum, mais rápido).
- `--timeout` e `--tentativas` controlam a espera por consulta.
- Sem internet: mensagem clara e código de saída 1, sem traceback.
- AP e DF ainda não estão no mapeamento de UF do SICOR (código interno do BCB não validado).
- Limites do dado: só contratos NOVOS do ano (não é saldo devedor nem inadimplência) e dado
  agregado, sem nome/CPF. Serve para segmentar anúncio institucional por região, nunca para
  abordar pessoas (Provimento 205/2021 da OAB).

## 3. Exemplo completo (dados fictícios)

```
python main.py exemplo             (calculadora + radar fictício + teste de acesso à API do BCB)
python main.py exemplo --sem-rede  (nem tenta a API)
```
Termina OK mesmo sem internet.

## Configuração

`config_comercial.py`: nome do escritório, responsável, OAB, CNPJ, cidade/UF, telefone, site,
Instagram, número do WhatsApp da calculadora, cores (azul-marinho #1F2A44 + verde-oliva #6B7F3A) e
pesos/produtos do radar. Campos `[PREENCHER]` ainda não definidos não aparecem nas páginas, e o
botão do WhatsApp fica desligado até o número ser preenchido.

## Arquivos

| Arquivo | Função |
|---|---|
| `main.py` | CLI (`calculadora`, `radar`, `exemplo`) |
| `calculadora.py` | cálculo Price/SAC, carência, custo efetivo, cenário de prorrogação, relatório |
| `modelos/calculadora_pagina.html` | modelo da página interativa (não editar o bloco CONFIG) |
| `radar.py` | consolidação, índice, ranking de municípios e regiões, CSV/HTML/JSON |
| `sicor.py` | acesso à API Olinda (SICOR) e IBGE, só com urllib |
| `html_util.py` | HTML autocontido nas cores do escritório |
| `config_comercial.py` | dados do escritório e parâmetros |
| `exemplos/` | dados fictícios usados pelo `exemplo` |
