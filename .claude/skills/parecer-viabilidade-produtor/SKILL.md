---
name: parecer-viabilidade-produtor
description: "Faz o parecer de viabilidade do caso do produtor rural (triagem jurídica): operações, enquadramento no crédito rural, teses, riscos, caminho processual, documentos faltantes e urgências. Não é peça processual."
---

# parecer-viabilidade-produtor

Entrada: ficha/transcrição da conversa com o produtor, cédulas e extratos que houver, notificações
e respostas do banco, autos de execução/busca e apreensão já existentes.

Entregue `saida/PARECER_VIABILIDADE.md` com:
1. **Resumo em 5 linhas**: quem é o produtor, quanto deve, a quem, o que aconteceu, o que
   recomendamos.
2. **Quadro das operações** (uma linha por cédula): banco, nº, tipo de título, finalidade, fonte
   de recursos (controlado/livre, BNDES, fundos constitucionais, Pronaf/Pronamp), valor, saldo,
   vencimentos, taxa, garantias, avalistas, status (em dia, vencida, executada), já prorrogada?
   O que não constar dos documentos fica [PREENCHER].
3. **Enquadramento**: é crédito rural (ou rural pela destinação)? Justiça Estadual ou Federal
   (DNA 3.1)? Operação securitizada/PESA/cedida à União?
4. **Teses aplicáveis**, cada uma com o fundamento do DNA 6 e a força (forte/média/fraca):
   prorrogação (com o alerta da Res. CMN 5.314/2026), revisão de juros e mora, impenhorabilidade,
   venda casada, RJ do produtor (Tema 1145/STJ e Lei 11.101/05, arts. 48 e 49).
5. **Riscos**: sem pedido administrativo ou pedido em cima do vencimento; laudo genérico (sem ART,
   sem vistoria, sem dados da propriedade); CCB/CPR sem prova de destinação; operação já
   prorrogada; renegociação oferecida e recusada; operações adimplentes misturadas; produtor de
   grande porte (gratuidade contestada); capitalização pactuada (Súmula 93/STJ); sucumbência.
6. **Caminho recomendado** em passos: notificação (skill `notificacao-extrajudicial-banco`) →
   ação de prorrogação com tutela → embargos/agravo se houver execução, leilão ou busca e
   apreensão; ou RJ quando o endividamento é sistêmico.
7. **Urgências com data**: próximo vencimento, prazo de embargos/defesa em curso, leilão marcado,
   negativação que trava o custeio da safra.
8. **Documentos a pedir ao cliente**: cédulas e aditivos, extratos da conta vinculada, IR/LCDPR
   (3 anos), notas de produtor, GTAs ou registros de movimentação de rebanho, CCIR/ITR/CAR,
   matrícula do imóvel, laudo agronômico com ART, laudo de capacidade de pagamento, decretos de
   emergência, fotos e dados de produção/preço.
- Linguagem para o Dr. Daniel decidir; sem promessa de resultado ao cliente.
- Termina com `STATUS: AGUARDA REVISÃO DO DR. DANIEL`.

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
