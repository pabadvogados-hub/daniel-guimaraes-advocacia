---
name: agravo-instrumento
description: "Redige agravo de instrumento com pedido de efeito suspensivo ou antecipação da tutela recursal (art. 1.015 do CPC): tutela negada para suspender execução, leilão ou busca e apreensão, retirar nome de cadastro, ou decisão que rejeitou impenhorabilidade."
---

# agravo-instrumento

Prazo: 15 dias úteis da intimação (art. 1.003, §5º, do CPC). Cabimento: decisão sobre tutela
provisória (art. 1.015, I) ou outra hipótese do art. 1.015 (confira o inciso; na execução, toda
interlocutória é agravável — art. 1.015, parágrafo único) [CONFERIR].

Tribunal: TJ do Estado; TRF se a causa é da Justiça Federal (DNA 3.1).

Estrutura:
1. `EXCELENTÍSSIMO SENHOR DESEMBARGADOR PRESIDENTE DO EGRÉGIO TRIBUNAL DE JUSTIÇA DO ESTADO DE
   [PREENCHER]`; qualificação; "interpor AGRAVO DE INSTRUMENTO COM PEDIDO DE ANTECIPAÇÃO DA TUTELA
   RECURSAL" contra a decisão do juízo `[PREENCHER: vara/comarca]` no processo nº `[PREENCHER]`;
   agravado com CNPJ e endereço;
2. DA TEMPESTIVIDADE E DO CABIMENTO; DO PREPARO (ou gratuidade extensiva, art. 99, §7º)
   [CONFERIR preparo]; DA FORMAÇÃO DO INSTRUMENTO (autos eletrônicos, art. 1.017, §5º); nomes e
   endereços dos advogados (art. 1.016, IV);
3. SÍNTESE DA DEMANDA E DA DECISÃO AGRAVADA: o que foi pedido e o fundamento EXATO da decisão,
   transcrevendo o trecho principal;
4. DAS RAZÕES DE REFORMA: um tópico por fundamento da decisão, com as teses do DNA (6.1 a 6.3);
5. DO EFEITO SUSPENSIVO / ANTECIPAÇÃO DA TUTELA RECURSAL (art. 1.019, I): probabilidade, perigo
   concreto (data do leilão, safra que depende do crédito, máquina apreendida na colheita) e
   reversibilidade;
6. DOS PEDIDOS: conhecimento; tutela recursal com as medidas negadas (sob multa diária);
   comunicação ao juízo de origem; intimação do agravado (art. 1.019, II); provimento.
- Leilão com data marcada: sinalize URGENTE no RESUMO e peça despacho antes da data.
- Sempre `STATUS: AGUARDA REVISÃO DO DR. DANIEL`.

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
