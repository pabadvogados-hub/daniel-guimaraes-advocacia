---
name: contrarrazoes-apelacao
description: Redige contrarrazões à apelação do banco (art. 1.010, §1º, do CPC) e, com adaptação, contraminuta a agravo de instrumento do banco (art. 1.019, II).
---

# contrarrazoes-apelacao

Prazo: 15 dias úteis (contrarrazões à apelação, art. 1.010, §1º; contraminuta ao agravo, art.
1.019, II) [CONFERIR redação]. Vale a intimação endereçada ao nosso cliente.

Estrutura (apelação): interposição curta ao juízo de origem + razões com o cabeçalho do DNA 3.4,
o banco como APELANTE e o produtor como APELADO, saudação `COLENDA CÂMARA,`:
1. síntese do processo, da sentença e do recurso;
2. preliminares contra o recurso, se houver: intempestividade, deserção (preparo), falta de
   dialeticidade (art. 932, III), inovação recursal;
3. DA MANUTENÇÃO DA SENTENÇA, um tópico por capítulo atacado pelo banco, rebatendo com a prova dos
   autos e a própria sentença. Defesas típicas dos bancos e como rebater:
   - "prorrogação é faculdade" → Súmula 298/STJ e DNA 6.1 (com a ressalva do MCR vigente);
   - "cerceamento de defesa" → banco fez protesto genérico de provas, prova técnica já nos autos;
   - "operação já prorrogada / pedido intempestivo / laudo genérico" → fatos e laudos do caso;
   - "CCB/CPR não é crédito rural" → destinação dos recursos (DNA 6.1);
4. DOS HONORÁRIOS RECURSAIS (art. 85, §11);
5. DOS PEDIDOS: não conhecimento ou desprovimento; manutenção da tutela; majoração dos honorários.
- Contraminuta ao agravo: dirigida ao relator, mesma lógica, pedindo a manutenção da decisão.
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
