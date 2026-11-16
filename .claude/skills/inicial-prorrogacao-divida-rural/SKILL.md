---
name: inicial-prorrogacao-divida-rural
description: Redige a petição inicial da ação de prorrogação/alongamento de dívida rural (com ou sem revisão de cláusulas) com pedido de tutela de urgência, a partir da ficha, da notificação ao banco, das cédulas e dos laudos.
---

# inicial-prorrogacao-divida-rural

Carro-chefe do escritório. Pressupõe, em regra, notificação extrajudicial já enviada (skill
`notificacao-extrajudicial-banco`) e sem resposta ou com recusa.

Escolha da justiça (DNA 3.1): Caixa, BNDES no polo ou União (crédito cedido) → Justiça Federal;
demais bancos e cooperativas → Vara Cível estadual.

Estrutura:
1. endereçamento (DNA 3.2) e qualificação completa do produtor (PF e, se houver, a PJ rural);
2. "por seus advogados (procuração anexa), vem respeitosamente perante Vossa Excelência propor a
   presente" → título em linha própria, ex.: `AÇÃO DE PRORROGAÇÃO DE DÍVIDA RURAL C/C REVISÃO DE
   CLÁUSULAS CONTRATUAIS E PEDIDO DE TUTELA DE URGÊNCIA` → "em face de" o banco;
3. DA GRATUIDADE DA JUSTIÇA (ou do diferimento/parcelamento das custas);
4. DOS FATOS: perfil do produtor e da propriedade; quadro das operações (DNA 2); evento adverso
   com período e prova (laudo, decretos, dados oficiais); produção e receita projetadas x obtidas;
   capacidade de pagamento futura (ano de retomada, nº de parcelas) tirada do laudo; pedido
   administrativo (data, canal, resposta ou silêncio);
5. DO DIREITO: Súmula 298/STJ; MCR 2-6-4 com a redação vigente conferida (DNA 6.1); Lei 4.829/65 e
   Lei 8.171/91, art. 50, V; natureza rural pela destinação quando houver CCB/CPR; ônus do banco de
   motivar a negativa e provar o requisito faltante; exibição das cédulas (arts. 396 a 400 do CPC);
6. (se c/c revisão) DA REVISÃO: juros remuneratórios acima de 12% a.a. sem fixação do CMN; juros
   de mora acima de 1% a.a. (DL 167/67, art. 5º, p.u.); capitalização sem pactuação clara (cuidado,
   DNA 6.2); seguros/títulos impostos (DNA 6.4); descaracterização da mora (DNA 6.2);
7. DA TUTELA DE URGÊNCIA (art. 300 do CPC): probabilidade (laudos + pedido não atendido + Súmula
   298), perigo (negativação trava o custeio da próxima safra; execução e constrição de bens de
   produção), reversibilidade (banco mantém as garantias). Pedidos: suspensão da exigibilidade das
   operações, com extensão aos avalistas; abstenção/baixa de negativação (SERASA, SPC,
   SCR/Registrato); vedação de protesto, vencimento antecipado, execução, busca e apreensão e
   constrição; manutenção dos bens empenhados com o produtor como depositário; multa diária;
8. DOS PEDIDOS em alíneas (tutela; citação; procedência para declarar o direito à prorrogação
   nas condições do laudo — carência + parcelas, mantidos os encargos ou só os legalmente
   exigíveis; revisão; exibição; inversão do ônus só se houver base, DNA 6.5; provas; custas e
   honorários), pedido de intimação exclusiva, valor da causa (soma das operações).
- Toda taxa, saldo, data e número de operação sai das cédulas/extratos; sem eles, [PREENCHER].
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
