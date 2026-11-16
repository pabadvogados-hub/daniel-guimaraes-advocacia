---
name: replica
description: Redige a réplica do produtor (manifestação sobre a contestação do banco e os documentos), arts. 350 e 351 do CPC, 15 dias úteis.
---

# replica

Abertura: "... apresentar RÉPLICA À CONTESTAÇÃO, impugnando os fatos, fundamentos e documentos
apresentados pelo Réu, pelos motivos de fato e de direito a seguir expostos:".

Estrutura:
1. DA TEMPESTIVIDADE (15 dias úteis, arts. 350 e 351 do CPC);
2. DA SÍNTESE DA CONTESTAÇÃO;
3. DAS PRELIMINARES: um tópico por preliminar, na ordem da defesa (impugnação à gratuidade,
   inépcia do pedido revisional, falta de interesse por ausência de pedido administrativo,
   litispendência x prejudicialidade, incompetência, ilegitimidade);
4. DO MÉRITO, ponto a ponto, repetindo no título a tese do banco ("DA ALEGADA FACULDADE DA
   INSTITUIÇÃO FINANCEIRA", "DO SUPOSTO PEDIDO INTEMPESTIVO", "DA ALEGADA NATUREZA COMERCIAL DA
   CCB", "DO LAUDO TÉCNICO", "DA OPERAÇÃO JÁ PRORROGADA") e rebatendo com o DNA 6 e a prova;
   lembre o ônus do banco de provar qual requisito faltou (art. 373, II, do CPC);
5. DOS DOCUMENTOS: impugne os documentos do banco que contrariam a inicial (planilhas sem memória,
   telas sistêmicas, propostas não assinadas);
6. DOS PEDIDOS: rejeição das preliminares; manutenção da tutela; procedência; produção das provas
   (perícia contábil e agronômica, exibição de documentos); sucumbência.

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
