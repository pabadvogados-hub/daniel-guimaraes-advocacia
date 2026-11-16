---
name: embargos-execucao-cedula-rural
description: "Redige embargos à execução (título extrajudicial: cédula rural, CCB, CPR, nota promissória rural) do produtor executado, com efeito suspensivo, excesso de execução, impenhorabilidade e prejudicialidade com a ação de prorrogação. Também serve de base para impugnação ao cumprimento de sentença."
---

# embargos-execucao-cedula-rural

Prazo: **15 dias úteis da juntada aos autos do mandado de citação cumprido** (art. 915 c/c art.
231, II, do CPC) — não da publicação. Confira a data da juntada; sem ela, [PREENCHER]. Para
impugnação ao cumprimento de sentença: art. 525 do CPC, 15 dias após o prazo do art. 523.

Distribuição por dependência à execução (DNA 3.2). Estrutura:
1. DA TEMPESTIVIDADE;
2. DA SÍNTESE DA EXECUÇÃO: título (tipo, nº, data, valor), valor executado, vencimentos,
   garantias, avalistas executados; contexto produtivo e pedido de prorrogação feito (ou ação em
   curso, com número);
3. DA GRATUIDADE (ou custas ao final);
4. DO EFEITO SUSPENSIVO (art. 919, §1º): probabilidade + perigo + garantia do juízo (penhora,
   penhor/hipoteca do próprio título) ou [CONFERIR garantia do juízo];
5. DA PREJUDICIALIDADE EXTERNA (se houver ação de prorrogação/revisional): suspensão (art. 313, V,
   "a"), sem confundir com litispendência;
6. DO MÉRITO, um tópico por tese, só as que o caso sustenta:
   - natureza rural do crédito e direito à prorrogação (DNA 6.1): inexigibilidade nos vencimentos
     originais;
   - excesso de execução (art. 917, III e §3º): juros de mora acima de 1% a.a. (DL 167/67, art. 5º,
     p.u.), juros remuneratórios acima do limite, encargos sobre parcelas vincendas antecipadas,
     pagamentos parciais não descontados (DL 167/67, art. 10, §1º). Declare o valor que entende
     correto com memória de cálculo (skill `liquidacao-previa`) — sem isso a alegação de excesso
     pode ser rejeitada liminarmente (art. 917, §4º) [CONFERIR];
   - impenhorabilidade da pequena propriedade rural (DNA 6.3: Tema 961/STF e Tema 1234/STJ — o ônus
     de provar a exploração familiar é do executado; junte CCIR, módulo fiscal, ITR, notas);
   - nulidade de aval/garantia em nota promissória rural ou duplicata rural (DL 167/67, art. 60,
     §§ 2º e 3º);
   - descaracterização da mora (DNA 6.2);
   - extensão dos efeitos aos avalistas;
7. DOS PEDIDOS: recebimento; gratuidade; efeito suspensivo; suspensão por prejudicialidade;
   procedência (inexigibilidade/excesso, valor correto); perícia contábil; intimação do embargado
   (art. 920); provas; sucumbência.
- Alternativa a avaliar com o Dr. Daniel: parcelamento do art. 916 (depósito de 30% e o resto em
  até 6 parcelas, renunciando aos embargos) [CONFERIR] — nunca escolher sozinho.
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
