---
name: contestacao-produtor
description: Redige a contestação do produtor rural réu (ação de cobrança, monitória — como embargos monitórios —, busca e apreensão de máquina/implemento em alienação fiduciária, ação de banco ou trading).
---

# contestacao-produtor

Prazos (confira o termo inicial nos autos, não a publicação):
- procedimento comum: 15 dias úteis (art. 335 do CPC), contados da audiência de conciliação/
  mediação sem acordo ou da juntada do AR/mandado (art. 231) [CONFERIDO: planalto.gov.br];
- monitória: embargos monitórios em 15 dias (art. 702 do CPC) [CONFERIR];
- busca e apreensão (DL 911/69): purga da mora em 5 dias e resposta em 15 dias, contados da
  execução da liminar (art. 3º, §§ 2º e 3º) [CONFERIR] — avalie no mesmo dia o agravo de
  instrumento contra a liminar (skill `agravo-instrumento`).

Estrutura:
1. endereçamento com o nº do processo; abertura "... vem apresentar CONTESTAÇÃO" (ou EMBARGOS
   MONITÓRIOS);
2. DA TEMPESTIVIDADE; DA GRATUIDADE (se for o caso);
3. preliminares cabíveis (art. 337 do CPC): incompetência (Justiça Federal x Estadual, foro),
   inépcia, ilegitimidade, falta de interesse, conexão com a ação de prorrogação;
   (busca e apreensão) mora não comprovada — notificação inválida ou sem prova de entrega
   [CONFERIR PRECEDENTE];
4. DO MÉRITO, ponto a ponto contra a inicial do banco: natureza rural e direito à prorrogação
   (DNA 6.1); excesso e encargos (DNA 6.2); descaracterização da mora; essencialidade do bem para a
   safra (busca e apreensão) [CONFERIR PRECEDENTE]; seguros impostos (DNA 6.4);
5. reconvenção, se o caso pedir (prorrogação/revisão), em tópico próprio (art. 343);
6. DOS PEDIDOS: acolhimento das preliminares; improcedência; (busca e apreensão) revogação da
   liminar e restituição do bem; provas (perícia contábil e agronômica); sucumbência.
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
