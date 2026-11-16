# DNA DAS PEÇAS — Daniel Guimarães Advocacia

> **Nicho: defesa do PRODUTOR RURAL**, principalmente contra bancos e cooperativas de crédito:
> crédito rural, cédulas rurais, prorrogação/alongamento de dívida rural, execuções, busca e
> apreensão, revisional e recuperação judicial do produtor rural.
>
> **Versão inicial (16/11/2026), PROVISÓRIA.** A formatação (seção 2) e o estilo (seções 3 a 5)
> ainda são os herdados da base e valem **só até lermos 5 a 10 peças reais do Dr. Daniel**. Os
> dados do escritório (seção 1) ainda não chegaram: tudo que estiver em `[PREENCHER: ...]` trava o
> protocolo.

Todo prompt de produção e de revisão de peça lê este arquivo **antes** de escrever. Se ele mudar,
as peças mudam junto.

## 1. Quem assina e em nome de quem

- Sociedade/escritório: **DANIEL GUIMARÃES ADVOCACIA** `[PREENCHER: razão social exata]`,
  CNPJ `[PREENCHER: CNPJ]`, registro OAB `[PREENCHER: nº de registro da sociedade na OAB/UF]`,
  com sede em `[PREENCHER: endereço completo, cidade/UF, CEP]` (é onde recebe as intimações).
- Bloco de assinatura (uma linha por advogado, nome em CAIXA ALTA, travessão, OAB):
  ```
  DANIEL GUIMARÃES [PREENCHER: nome completo] – OAB/[PREENCHER: UF] [PREENCHER: nº]
  [PREENCHER: demais advogados da equipe – OAB/UF nº]
  ```
- Quem revisa e protocola: **Dr. Daniel Guimarães** `[CONFERIR: ou outro advogado da equipe]`.
- Na qualificação o escritório fala "**por seus advogados**" `[CONFERIR nas peças reais]`.
- Pedido de intimação exclusiva (fim de toda inicial e da primeira manifestação nos autos):
  "Requer que todas as intimações sejam feitas exclusivamente em nome de `[PREENCHER: advogado
  – OAB/UF nº]`, sob pena de nulidade (art. 272, §§ 2º e 5º, do CPC)."
- Local e data: a cidade da comarca, seguida de vírgula ("Cidade/UF, 16 de novembro de 2026.").
  Peça assinada digitalmente pode usar "Local e data da assinatura eletrônica." `[CONFERIR qual o
  escritório usa]`.

## 2. Formatação — PROVISÓRIA (herdada da base)

> Vale até lermos 5 a 10 peças reais do Dr. Daniel. Depois, troque fonte, recuo, cor e títulos
> pelo padrão dele e ajuste `ESC_FONTE_PECA`, `ESC_TAMANHO_PECA` e `ESC_RECUO_PECA_CM` no servidor.

- Fonte **Century Gothic 12**, corpo **justificado**, espaçamento 1,5.
- Recuo da primeira linha: **3 cm** nos parágrafos de texto. Endereçamento, títulos e assinatura
  ficam sem recuo.
- Títulos de tópico em **CAIXA ALTA e negrito**, começando por "DA/DO/DAS/DOS" ("DA PRORROGAÇÃO
  COMPULSÓRIA DA DÍVIDA RURAL", "DO EXCESSO DE EXECUÇÃO").
- Citação de lei, súmula ou norma do MCR em parágrafo próprio, dispositivo antes e texto entre
  aspas: `Art. 5º, parágrafo único, do Decreto-Lei nº 167/67: "Em caso de mora, a taxa de juros
  constante da cédula será elevável de 1% (um por cento) ao ano."`
- Pedidos em alíneas `a)`, `b)`, `c)`, cada uma terminando em ponto e vírgula, a última em ponto.
- Tabela das operações (banco, nº da cédula, tipo de título, finalidade, fonte de recursos, valor,
  saldo, vencimentos, juros, garantias, avalistas) entra como lista numerada no texto, uma
  operação por parágrafo, porque o timbrado é montado a partir de texto corrido.
- O papel é o **TIMBRADO.docx** (`juridico/modelos/`). A imagem fica no cabeçalho e o texto entra
  no corpo. Nunca recrie o cabeçalho. `[PREENCHER: timbrado real do escritório]`

## 3. Endereçamento e abertura

### 3.1 Qual justiça
- **Regra: Justiça Estadual**, Vara Cível da comarca (ou Vara Única/Genérica onde não houver Vara
  Cível; Vara Empresarial/de Falências quando a lei estadual de organização judiciária concentrar
  a recuperação judicial). Vale para Banco do Brasil, Banco da Amazônia, Banco do Nordeste
  (sociedades de economia mista), bancos privados, cooperativas de crédito e tradings.
  Base: Súmula 42/STJ (sociedade de economia mista é julgada na Justiça Comum Estadual)
  `[CONFERIR texto oficial da súmula]`.
- **Justiça Federal** (Vara Federal Cível da Subseção Judiciária do domicílio do produtor ou da
  sede da agência), quando for parte **empresa pública federal, União ou autarquia federal**
  (CF, art. 109, I): sobretudo **Caixa Econômica Federal**, **BNDES** quando figurar diretamente
  no polo, e a **União/PGFN** nos créditos rurais alongados ou renegociados com base na Lei
  9.138/95 que foram cedidos à União (MP 2.196-3/2001, art. 2º) e hoje são cobrados como dívida
  ativa `[CONFERIR em cada caso se a operação foi cedida à União]`. Recurso vai ao TRF da região.
- Se o banco público federal não está no polo (ex.: BB operando recurso do BNDES ou de fundo
  constitucional), a ação continua na Justiça Estadual.
- Foro: domicílio do produtor quando houver relação de consumo discutida, senão foro de eleição
  da cédula ou sede da agência `[CONFERIR cláusula de eleição de foro]`.

### 3.2 Endereçamento (provisório, no estilo da base)
- Primeira instância estadual: `AO JUÍZO DA [PREENCHER: nº]ª VARA CÍVEL DA COMARCA DE [PREENCHER:
  CIDADE] – [UF]` (sem "EXCELENTÍSSIMO", sem "MM." até vermos as peças reais).
- Primeira instância federal: `AO JUÍZO DA [PREENCHER: nº]ª VARA FEDERAL CÍVEL DA SUBSEÇÃO
  JUDICIÁRIA DE [PREENCHER] – [UF]`.
- Logo abaixo, nas manifestações: `Processo nº 0000000-00.0000.8.00.0000` (estadual, segmento 8)
  ou `.4.00.0000` (federal, segmento 4).
- Embargos à execução: `Distribuição por dependência ao processo nº [PREENCHER]`.

### 3.3 Abertura
- Manifestação nos autos:
  > {CLIENTE EM CAIXA ALTA}, já qualificado nos autos da {AÇÃO ...} nº {processo} que move em face
  > de {BANCO EM CAIXA ALTA} (ou "que lhe move"), por seus advogados, vem respeitosamente perante
  > Vossa Excelência apresentar {NOME DA PEÇA EM CAIXA ALTA}, pelos motivos de fato e de direito a
  > seguir expostos:
- Inicial: qualificação completa do produtor (nacionalidade, estado civil, profissão "produtor
  rural"/"pecuarista"/"agricultor", RG, CPF, inscrição estadual de produtor, endereço com CEP; se
  atua por PJ, razão social, CNPJ e representante), "por seus advogados (procuração anexa), vem
  respeitosamente perante Vossa Excelência propor a presente", então o nome da ação em linha
  própria em CAIXA ALTA — por exemplo `AÇÃO DE PRORROGAÇÃO DE DÍVIDA RURAL C/C REVISÃO DE
  CLÁUSULAS CONTRATUAIS E PEDIDO DE TUTELA DE URGÊNCIA` — e depois "em face de" o banco (razão
  social, CNPJ, sede e agência).
- Defesa: "... vem apresentar CONTESTAÇÃO" / "opor EMBARGOS À EXECUÇÃO" / "apresentar
  IMPUGNAÇÃO AO CUMPRIMENTO DE SENTENÇA".

### 3.4 Recursos cíveis
- **Apelação** (art. 1.009 do CPC; 15 dias úteis): petição de interposição dirigida ao juízo de
  origem (cabimento, tempestividade, preparo ou gratuidade, pedido de intimação do apelado e de
  remessa ao Tribunal) e depois as razões, com o cabeçalho:
  ```
  EGRÉGIO TRIBUNAL DE JUSTIÇA DO ESTADO DE [PREENCHER]
  APELANTE: …
  APELADO: …
  PROCESSO Nº: …
  ORIGEM: [Nª] VARA CÍVEL DA COMARCA DE …
  RAZÕES DE APELAÇÃO
  ```
  seguido da saudação `COLENDA CÂMARA,` (no TRF: `EGRÉGIO TRIBUNAL REGIONAL FEDERAL DA [N]ª
  REGIÃO` e `COLENDA TURMA,`).
- **Contrarrazões de apelação** (art. 1.010, §1º; 15 dias úteis): mesmo cabeçalho, com APELANTE
  (o banco) e APELADO (o produtor), terminando no pedido de desprovimento e de majoração dos
  honorários (art. 85, §11).
- **Agravo de instrumento** (art. 1.015; 15 dias úteis): dirigido direto ao Tribunal
  (`EXCELENTÍSSIMO SENHOR DESEMBARGADOR PRESIDENTE DO EGRÉGIO TRIBUNAL DE JUSTIÇA DO ESTADO DE
  ...`), com nome e endereço dos advogados (art. 1.016, IV), pedido de efeito suspensivo ou de
  antecipação da tutela recursal (art. 1.019, I) e informação de que os autos são eletrônicos
  (art. 1.017, §5º). Uso típico: tutela negada para suspender execução, leilão ou negativação.
- **Embargos de declaração** (arts. 1.022 e 1.023; **5 dias úteis**): petição única ao prolator,
  um tópico por vício; interrompem o prazo dos demais recursos (art. 1.026).
- **Recurso especial** (art. 105, III, CF; art. 1.029 do CPC; 15 dias úteis): interposição ao
  Presidente/Vice-Presidente do Tribunal de origem, com cabimento, prequestionamento e
  demonstração da violação a lei federal (DL 167/67, Lei 4.829/65, CPC) ou do dissídio
  jurisprudencial com cotejo analítico. Só com decisão expressa do Dr. Daniel.
- Prazos em **dias úteis** (art. 219 do CPC); sem prazo legal nem fixado pelo juiz, **5 dias**
  (art. 218, §3º).

## 4. Fecho

- Último tópico: `DOS PEDIDOS` (inicial, recursos), `DOS REQUERIMENTOS` (manifestações, ED,
  embargos) ou `DOS PEDIDOS E REQUERIMENTOS`.
- Antes do fecho, na inicial e nos embargos: protesto de provas (documental, pericial contábil e
  agronômica, testemunhal, depoimento pessoal do representante do banco), pedido de intimação
  exclusiva e `Dá-se à causa o valor de R$ … (por extenso).` (na prorrogação/revisional: a soma
  das operações discutidas, art. 292, II, do CPC `[CONFERIR critério do Dr. Daniel]`).
- Fórmula de fecho, em linha própria: **`Termos em que, pede deferimento.`** `[CONFERIR]`
- Depois a cidade e a data, e por fim o bloco de assinatura do item 1.

## 5. Tom e construção do argumento

- Tom técnico e direto; o produtor é apresentado como quem produz e quer pagar **com produção, não
  com o patrimônio**. Sem adjetivação excessiva nem latim gratuito.
- Narrativa dos fatos sempre com **dados concretos**: área (ha), atividade (soja, milho, café,
  pecuária de corte/leite), safra afetada, evento (estiagem, excesso de chuva, geada, granizo,
  praga, queda de preço), **produção e receita projetadas x obtidas**, decretos de emergência,
  laudo agronômico e laudo de capacidade de pagamento.
- Uma operação por linha: nº da cédula, tipo (CCR, cédula rural pignoratícia/hipotecária, nota de
  crédito rural, CPR, CCB com destinação rural), finalidade, fonte de recursos (controlados,
  livres, BNDES, FNO/FNE/FCO, Pronaf/Pronamp), valor, saldo, vencimentos, garantias e avalistas.
- Na resposta ao banco, **rebater ponto a ponto**: primeiro o que ele alega ("O Réu sustenta
  que…"), depois por que não se sustenta. Frases curtas de virada em parágrafo próprio ("Ao
  contrário.", "Isso porque…", "Portanto, …").
- Ancorar cada tópico em dispositivo (DL 167/67, Lei 4.829/65, Lei 8.171/91, MCR, CPC, CC, CDC
  quando cabível) e, quando houver, em súmula ou tema repetitivo **conferido** (seção 6).
- O direito à prorrogação tem base própria (crédito rural); CDC entra como reforço, nunca como
  fundamento único ("ainda que se afaste o CDC, o pedido subsiste").
- Pedido cautelar: "Por cautela, registra-se que…".

## 6. Teses recorrentes (defesa do produtor rural)

Legenda: **[CONFERIDO: fonte]** = texto conferido em fonte oficial em 16/11/2026;
**[CONFERIR]** = conferir redação/número antes de citar; **[CONFERIR PRECEDENTE]** = a IA não cita
julgado específico sem fonte conferida. Nenhum número de processo, data ou ementa pode ser criado.

### 6.1 Prorrogação/alongamento da dívida rural (tese central)
- **Súmula 298/STJ**: "O alongamento de dívida originada de crédito rural não constitui faculdade
  da instituição financeira, mas, direito do devedor nos termos da lei." [CONFERIDO: Arquivo do
  STJ, verbete de 18/10/2004 — conferir pontuação no portal de súmulas]. Usar sempre que houver
  frustração de safra/receita e pedido de prorrogação negado ou sem resposta.
- **MCR, Capítulo 2, Seção 6, item 4 (MCR 2-6-4)**: prorrogação mantidos os encargos, quando o
  mutuário comprova dificuldade temporária de reembolso por a) dificuldade de comercialização,
  b) frustração de safra por fatores adversos, c) ocorrências prejudiciais ao desenvolvimento das
  explorações (e, pela redação de 2025, d) perdas acumuladas de safras anteriores) [CONFERIR].
  **ATENÇÃO:** a Resolução CMN nº 5.314, de 25/06/2026 (vigência noticiada em 01/07/2026), teria
  alterado o item 2-6-4 para dizer que a instituição fica autorizada "por sua conveniência e
  decisão" a prorrogar [CONFERIR no site do BCB — não localizamos o texto oficial]. Até conferir:
  (i) transcrever o MCR só com a redação vigente na data do pedido/do vencimento, citando a
  resolução que a deu; (ii) para fatos e pedidos anteriores à mudança, sustentar a redação então
  vigente; (iii) em qualquer caso, apoiar o direito na Súmula 298/STJ e na lei (abaixo), e exigir
  do banco negativa **motivada** e prova de que o requisito não foi cumprido.
- **Lei 4.829/65**: art. 1º (crédito rural voltado ao "bem-estar do povo"), art. 2º (conceito:
  recursos "para aplicação exclusiva em atividades que se enquadrem nos objetivos indicados na
  legislação em vigor"), art. 3º, III ("possibilitar o fortalecimento econômico dos produtores
  rurais, notadamente pequenos e médios") e art. 14 (prazos, juros e condições estabelecidos pelo
  CMN) [CONFERIDO: planalto.gov.br]. Usar para a natureza pública/de fomento do crédito rural.
- **Lei 8.171/91, art. 50, V**: "prazos e épocas de reembolso ajustados à natureza e
  especificidade das operações rurais, bem como à capacidade de pagamento e às épocas normais de
  comercialização…" [CONFERIDO: planalto.gov.br]. Usar para pedir cronograma compatível com a
  safra e com o laudo de capacidade de pagamento.
- **Lei 9.138/95, art. 5º**: autoriza o alongamento de dívidas de crédito rural **contratadas até
  20 de junho de 1995** (custeio, investimento, comercialização, fundos constitucionais da Lei
  7.827/89, FAT, Funcafé), com limite de R$ 200.000,00 por emitente [CONFERIDO:
  planalto.gov.br]. **Não serve de base para operação nova**: usar só para operações daquela
  época (securitização) ou como reforço histórico da natureza obrigatória do alongamento.
- **Pedido administrativo prévio**: o caminho padrão é notificar o banco antes da ação (skill
  `notificacao-extrajudicial-banco`), com laudos; silêncio = pretensão resistida. Se o pedido foi
  feito após o vencimento, sustentar que a norma não fixa prazo preclusivo [CONFERIR redação
  vigente do MCR e PRECEDENTE].
- **Suspensão da execução enquanto se discute o alongamento**: existe orientação do STJ nesse
  sentido [CONFERIR PRECEDENTE]. Pedir tutela de urgência (art. 300 do CPC) para suspender a
  exigibilidade, vedar negativação (SERASA, SPC, SCR/Registrato), protesto, execução e
  constrição, com extensão aos avalistas.
- **Natureza rural pela destinação** (CCB, CPR com liquidação financeira, "capital de giro"
  usados na lavoura/pecuária): o que define o regime é a destinação dos recursos (Lei 4.829/65,
  art. 2º) [CONFERIR PRECEDENTE]. Exige prova da aplicação (notas, GTAs, projeto, extratos).

### 6.2 Juros, capitalização e encargos de mora na cédula rural
- **Juros remuneratórios limitados a 12% a.a.** nas cédulas de crédito rural quando o CMN não fixa
  a taxa (DL 167/67, art. 5º, caput — juros "às taxas que o Conselho Monetário Nacional fixar"
  [CONFERIDO: planalto.gov.br] — c/c Decreto 22.626/33). Jurisprudência do STJ firme, mas sem
  súmula nem tema repetitivo localizado [CONFERIR PRECEDENTE]. Usar na revisional e no excesso de
  execução, principalmente em operações com recursos livres e em CCB de destinação rural.
- **Juros de mora**: DL 167/67, art. 5º, parágrafo único: "Em caso de mora, a taxa de juros
  constante da cédula será elevável de 1% (um por cento) ao ano." [CONFERIDO: planalto.gov.br].
  Usar para afastar juros moratórios mensais, comissão de permanência e "taxa de inadimplência"
  cumulada; a multa contratual é discutida à parte [CONFERIR].
- **Capitalização**: DL 167/67, art. 5º, caput, permite exigir os juros em 30/06 e 31/12 ou no
  vencimento e "capitalizar tais encargos na conta vinculada" [CONFERIDO: planalto.gov.br].
  Súmula 93/STJ admite o pacto de capitalização nas cédulas rurais, e há repetitivo admitindo
  periodicidade inferior à semestral se pactuada [CONFERIR texto e número do tema]. **Risco**:
  não atacar capitalização expressamente pactuada sem parecer contábil; foco em falta de pactuação
  clara (taxa anual x mensal) e em encargos fora do período de normalidade.
- **Descaracterização da mora**: o reconhecimento de abusividade nos encargos do período de
  normalidade (juros remuneratórios/capitalização) descaracteriza a mora (REsp 1.061.530/RS,
  repetitivo, Orientação 2 — identificado como Tema 28) [CONFERIR redação e número do tema].
  Usar para afastar mora, multa e negativação, e reforçar a tutela.
- **Correção monetária e índices**: conferir o índice pactuado e a série do BCB aplicável antes de
  alegar abusividade [CONFERIR].

### 6.3 Defesa na execução, penhora e garantias
- **Embargos à execução** (arts. 914 e seguintes do CPC; 15 dias úteis da juntada do mandado
  cumprido, art. 915 c/c art. 231, II [CONFERIDO art. 231: planalto.gov.br]); efeito suspensivo
  (art. 919, §1º); excesso de execução com valor correto e memória (art. 917, §3º); se houver
  ação de prorrogação em curso, suspensão por prejudicialidade externa (art. 313, V, "a").
- **Impenhorabilidade da pequena propriedade rural** (CF, art. 5º, XXVI; CPC, art. 833, VIII):
  STF, **Tema 961** (ARE 1.038.507) — a pequena propriedade rural trabalhada pela família é
  impenhorável **mesmo quando dada em garantia hipotecária**; abrange mais de um terreno se
  contínuos e com área total inferior a 4 módulos fiscais [CONFERIR redação oficial da tese no
  portal do STF — conferido só em fontes secundárias]. STJ, **Tema 1234** (REsp 2.080.023/MG):
  é ônus do **executado** provar que o imóvel é explorado pela família [CONFERIR redação oficial].
  Usar na impugnação à penhora (art. 917, §1º: 15 dias da ciência) e nos embargos; juntar CCIR,
  módulo fiscal do município, ITR, notas de produtor, DAP/CAF.
- **Garantias nulas em título rural**: DL 167/67, art. 60, §§ 2º e 3º — é nulo o aval dado em
  **nota promissória rural ou duplicata rural**, e nulas outras garantias, salvo quando prestadas
  por pessoas físicas participantes da empresa emitente, por esta ou por outras pessoas jurídicas;
  o §4º afasta a regra nas transações entre produtores e entre estes e suas cooperativas
  [CONFERIDO: planalto.gov.br]. Usar para avalistas e garantidores **nesses títulos**; não
  estender à cédula de crédito rural sem precedente [CONFERIR PRECEDENTE].
- **Cédula rural é título civil, líquido e certo** (DL 167/67, art. 10, redação da Lei
  13.986/2020) [CONFERIDO: planalto.gov.br] — atenção: favorece a executividade; a defesa ataca
  liquidez pelo excesso (pagamentos parciais devem ser descontados, art. 10, §1º).
- **Busca e apreensão de máquinas/implementos em alienação fiduciária** (DL 911/69): purga da mora
  com pagamento da integralidade da dívida pendente em 5 dias e resposta em 15 dias, ambos da
  execução da liminar (art. 3º, §§ 2º e 3º) [CONFERIR redação no Planalto — página indisponível
  na conferência]. Teses: natureza rural do crédito e direito à prorrogação, mora não
  configurada (notificação inválida, encargos abusivos), essencialidade do bem à safra.
- **Leilão do imóvel ou do bem**: agravo de instrumento/tutela para suspender, impenhorabilidade,
  nulidade da intimação do executado sobre o leilão (art. 889 do CPC) [CONFERIR], preço vil.

### 6.4 Seguros, venda casada e títulos de capitalização
- **Tema 972/STJ** (REsp 1.639.320/SP): nos contratos bancários em geral, o consumidor não pode ser
  compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada
  [CONFERIR redação oficial — conferido só em fontes secundárias]. Vale em relação de consumo
  (ver 6.5). Usar para restituir seguro prestamista, seguro de penhor "da casa", título de
  capitalização e consórcio impostos como condição do crédito (CDC, art. 39, I).
- Juntar a prova da imposição (mesma data, débito na operação, ausência de escolha da seguradora).

### 6.5 CDC: quando aplica ao produtor
- Posição predominante: crédito rural tomado para a produção é **insumo** da atividade, e o
  produtor não é destinatário final (teoria finalista) — CDC **não se aplica** em regra
  [CONFERIR PRECEDENTE do STJ]. Exceção: **finalismo mitigado**, com vulnerabilidade técnica,
  jurídica ou econômica demonstrada (pequeno produtor, contrato de adesão, venda casada)
  [CONFERIR PRECEDENTE]. No seguro agrícola o STJ já reconheceu o agricultor como destinatário
  final [CONFERIR PRECEDENTE].
- Súmula 297/STJ ("O Código de Defesa do Consumidor é aplicável às instituições financeiras")
  [CONFERIR texto] — usar com a ressalva acima.
- Regra de redação: o CDC é **reforço**. O direito à prorrogação, a limitação dos juros e dos
  encargos de mora têm base na legislação do crédito rural, independente do CDC.

### 6.6 Securitização, PESA e renegociações legais
- Operações alongadas pela **Lei 9.138/95** (securitização) e pelo **PESA** (Programa Especial de
  Saneamento de Ativos, Res. CMN 2.471/98) [CONFERIR número e redação]. Parte desses créditos foi
  cedida à **União** (MP 2.196-3/2001, art. 2º) [CONFERIR redação]: cobrança passa à PGFN, com
  competência da Justiça Federal e defesa em execução fiscal (prescrição, encargos, Lei 6.830/80).
- Leis de renegociação periódicas (ex.: Lei 11.775/2008, Lei 13.340/2016 e posteriores) e
  resoluções do CMN com descontos/liquidação [CONFERIR vigência e prazo de adesão]. Sempre
  verificar se há janela de adesão aberta antes de litigar.

### 6.7 Recuperação judicial do produtor rural
- **Lei 11.101/05 após a Lei 14.112/2020** [CONFERIDO: planalto.gov.br]: art. 48, §§ 2º a 5º
  (comprovação dos 2 anos de atividade rural: pela ECF na PJ; na PF pelo Livro Caixa Digital do
  Produtor Rural — LCDPR —, DIRPF e balanço patrimonial); art. 49, § 6º (só os créditos decorrentes
  exclusivamente da atividade rural, discriminados nesses documentos, sujeitam-se à RJ), § 7º
  (não se sujeitam os **recursos controlados** — arts. 14 e 21 da Lei 4.829/65), § 8º (sujeitam-se
  se não renegociados antes do pedido, na forma de ato do Poder Executivo), § 9º (fica fora a
  dívida dos 3 anos anteriores ao pedido para aquisição de propriedade rural e suas garantias).
- **Tema 1145/STJ** (REsp 1.905.573/MT e REsp 1.947.011/PR, 2ª Seção, j. 22/06/2022): "Ao produtor
  rural que exerça sua atividade de forma empresarial há mais de dois anos é facultado requerer a
  recuperação judicial, desde que esteja inscrito na Junta Comercial no momento em que formalizar
  o pedido recuperacional, independentemente do tempo de seu registro." [CONFERIDO: portal de
  repetitivos do STJ]. Usar na triagem: inscrição na Junta antes do pedido; prova dos 2 anos pelo
  LCDPR/IR.
- Plano simplificado para dívidas até o limite legal (art. 70-A) [CONFERIR].

### 6.8 CPR (Cédula de Produto Rural)
- Lei 8.929/94 (com as alterações da Lei 13.986/2020): CPR física e com liquidação financeira
  [CONFERIR artigos]. Teses: CPR "de gaveta"/financeira usada como crédito disfarçado (natureza de
  financiamento → regime e encargos do crédito rural) [CONFERIR PRECEDENTE]; frustração de safra
  por caso fortuito na CPR física [CONFERIR PRECEDENTE]; excesso por preço de referência; RJ: a
  CPR física com antecipação de preço tem regra própria (art. 11 da Lei 8.929/94) [CONFERIR].

### 6.9 Processuais recorrentes
- Gratuidade (arts. 98 e 99 do CPC): patrimônio rural é imobilizado, receita bruta não é liquidez;
  subsidiário: diferimento/parcelamento das custas [CONFERIR lei de custas estadual].
- Exibição de documentos pelo banco (arts. 396 a 400 do CPC): todas as cédulas, aditivos,
  extratos da conta vinculada e memória de cálculo.
- Ônus da prova: o banco prova o fato impeditivo (art. 373, II) e qual requisito do MCR faltou.
- Perícia contábil e agronômica; laudo técnico com ART e vistoria evita a principal crítica dos
  bancos (laudo genérico, sem ART, sem vistoria in loco).
- Réplica em 15 dias (art. 350 [CONFERIDO: planalto.gov.br] e art. 351).

## 7. Regra de ouro da automação

- **A IA decide sozinha** só em caso simples e padronizado e em petição de andamento (ciência,
  juntada, manifestação genérica sem tese, pedido de prazo, ED de omissão evidente).
- Tudo o mais (notificação ao banco, inicial, tutela de urgência, contestação, embargos à
  execução, réplica com tese nova, recursos, contrarrazões, acordo/renegociação, RJ) **para para
  revisão do Dr. Daniel** antes de protocolar ou enviar.
- A IA nunca inventa jurisprudência. Se o precedente não estiver neste DNA como **[CONFERIDO]**
  ou na base conferida, ela marca `[CONFERIR PRECEDENTE]` e segue. Nunca cria número de
  processo, relator, data ou ementa.
- A IA nunca inventa dado do cliente, da cédula ou do processo (nº da operação, taxa, saldo,
  vencimento, área, produção). Se faltar, deixa `[PREENCHER: campo]`, e a peça com marcação
  aberta não sai para protocolo.
- Norma do CMN/MCR: transcrever só a redação conferida e vigente na data relevante, citando a
  resolução; na dúvida, `[CONFERIR redação do MCR]`.
