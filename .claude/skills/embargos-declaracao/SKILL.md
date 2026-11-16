---
name: embargos-declaracao
description: Redige embargos de declaração (omissão, contradição, obscuridade, erro material) contra decisão, sentença ou acórdão cível — arts. 1.022 e 1.023 do CPC, 5 dias úteis.
---

# embargos-declaracao

Fundamento: arts. 1.022 e 1.023 do CPC. Prazo de **5 dias úteis** (art. 1.023), dirigidos ao
próprio prolator. Interrompem o prazo dos demais recursos (art. 1.026) [CONFERIR redação].

Abra um tópico por vício ("DA OMISSÃO QUANTO AO PEDIDO DE PRORROGAÇÃO DAS OPERAÇÕES ...", "DA
CONTRADIÇÃO ENTRE A FUNDAMENTAÇÃO E O DISPOSITIVO"), transcrevendo o pedido ou a tese que ficou
sem resposta e o trecho da decisão. Usos típicos no agro: sentença que reconhece a prorrogação mas
não fixa carência/parcelas/encargos; omissão sobre extensão aos avalistas; omissão sobre
limitação dos juros de mora (DL 167/67, art. 5º, p.u.); prequestionamento para recurso especial.

Feche em DOS REQUERIMENTOS, pedindo que o vício seja sanado, com efeitos infringentes quando a
correção mudar o resultado (nesse caso o embargado é intimado, art. 1.023, §2º). Não use ED para
rediscutir a prova (risco de multa por embargos protelatórios, art. 1.026, §2º).

ED por omissão evidente é petição simples e pode sair direto (regra de ouro); o resto vai ao Dr.
Daniel.

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
