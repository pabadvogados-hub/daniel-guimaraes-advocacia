---
name: liquidacao-previa
description: "Monta a memória de cálculo do caso agro: saldo devedor revisado, excesso de execução (art. 917, §3º), valor incontroverso da revisional, valor da causa e liquidação/cumprimento de sentença."
---

# liquidacao-previa

Entregue `saida/MEMORIA_CALCULO.md` (ou .xlsx) com, para cada operação: valor liberado e datas,
taxa contratada x taxa admitida (limite do DNA 6.2), juros de mora contratados x 1% a.a. (DL
167/67, art. 5º, p.u.), capitalização aplicada, seguros/tarifas/IOF financiados, pagamentos
feitos, saldo do banco x saldo recalculado e a diferença. Feche com o somatório.

Usos:
- embargos à execução: valor que o executado entende correto, com demonstrativo (art. 917, §3º);
- impugnação ao cumprimento (art. 525, §4º) [CONFERIR];
- revisional: valor incontroverso (art. 330, §§ 2º e 3º) [CONFERIR];
- valor da causa (soma das operações discutidas);
- liquidação/cumprimento de sentença a favor do produtor (repetição do indébito, honorários).

Dados só das cédulas, extratos e planilhas do banco; o que faltar vira [PREENCHER]. Não invente
índice: correção e juros seguem o título ou o critério da decisão, indicado por escrito. Cálculo
complexo vai ao contador/perito e a memória registra isso.

## Antes de escrever
1. Leia INTEIRO o `SISTEMA/backend/app/juridico/DNA_ESCRITORIO.md` (na raiz do repositório do sistema; no servidor, `$ESC_RAIZ/SISTEMA/backend/app/juridico/DNA_ESCRITORIO.md`).
   Ele define a justiça e o endereçamento (Estadual x Federal), a abertura ("por seus advogados"),
   os títulos DA/DO, as teses conferidas (seção 6), o fecho ("Termos em que, pede deferimento."),
   a cidade e data e o bloco de assinatura. A formatação dele é PROVISÓRIA: siga-a mesmo assim.
2. Leia todos os insumos da pasta do caso: cédulas e aditivos, extratos da conta vinculada,
   notificações e respostas do banco, laudos (agronômico e de capacidade de pagamento), autos,
   decisão e peça contrária. Imagem e PDF escaneado se leem por visão.

## Regras inegociáveis
- Nunca invente jurisprudência. Só cite o que está no DNA como [CONFERIDO] ou nos autos; o resto
  vira `[CONFERIR PRECEDENTE]`. Nunca crie número de processo, relator, data ou ementa.
- Nunca invente dado do cliente, da cédula ou do processo (nº da operação, taxa, saldo,
  vencimento, área, produção). O que faltar vira `[PREENCHER: campo]`.
- Norma do CMN/MCR só com a redação conferida e vigente na data relevante; na dúvida,
  `[CONFERIR redação do MCR]` (atenção à Res. CMN 5.314/2026, DNA 6.1).
- Valores sempre com "R$" e conferidos (a soma das operações tem de bater com o valor indicado).
- Prazos processuais em dias úteis (art. 219 do CPC).
- Rebata a peça contrária ponto a ponto: o que ela diz e por que não se sustenta.
- Regra de ouro (DNA, seção 7): só petição de andamento e caso simples saem direto. O resto
  termina com `STATUS: AGUARDA REVISÃO DO DR. DANIEL`.

## Entrega
- Monte o .docx no timbrado com a skill `timbrado`:
  `python .claude/skills/timbrado/montar_peca.py --texto saida/PECA.txt --saida "saida/<NOME>.docx"`
- Registre em `saida/RESUMO.txt`, em até 5 linhas, a peça, as teses usadas, os prazos e os pontos
  que pedem conferência ([PREENCHER] e [CONFERIR] que ficaram abertos).
