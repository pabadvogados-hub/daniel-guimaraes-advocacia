---
name: apelacao-civel
description: Redige apelação cível do produtor (art. 1.009 do CPC) contra sentença em ação de prorrogação, revisional, embargos à execução, busca e apreensão ou cobrança.
---

# apelacao-civel

Prazo: 15 dias úteis (art. 1.003, §5º, do CPC); se houver embargos de declaração, recomeça depois
da decisão deles (art. 1.026). Verifique preparo e porte de remessa (art. 1.007) ou gratuidade
[CONFERIR preparo].

Duas partes:
1. **Interposição**, dirigida ao juízo de origem: cabimento, tempestividade, preparo/gratuidade,
   pedido de intimação do apelado para contrarrazões e de remessa ao Tribunal; fecho e assinatura.
2. **Razões**, com o cabeçalho do DNA 3.4 (APELANTE/APELADO/PROCESSO/ORIGEM/RAZÕES DE APELAÇÃO) e
   `COLENDA CÂMARA,`:
   - síntese da demanda e da sentença;
   - preliminares, se houver (nulidade por cerceamento de defesa — perícia agronômica/contábil
     indeferida —, sentença extra/citra petita, ausência de fundamentação, art. 489, §1º);
   - um tópico por capítulo da sentença atacado (dialeticidade: rebater o fundamento exato),
     com as teses do DNA 6;
   - pedido de efeito suspensivo quando a sentença revoga tutela (art. 1.012, §§ 1º, V, e 4º)
     [CONFERIR];
   - DOS PEDIDOS: conhecimento e provimento, reforma de cada capítulo, inversão da sucumbência.
- Prequestione expressamente os dispositivos federais (DL 167/67, Lei 4.829/65, Lei 8.171/91, CPC)
  pensando no recurso especial.
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
