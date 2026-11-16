---
name: notificacao-extrajudicial-banco
description: Redige a notificação extrajudicial ao banco ou cooperativa pedindo a prorrogação/alongamento da dívida rural (MCR 2-6-4 e Súmula 298/STJ) e a entrega das cédulas. É o 1º passo antes da ação.
---

# notificacao-extrajudicial-banco

É a primeira peça do caso típico. Serve para (i) formar a prova do pedido administrativo (a
inércia ou a recusa sem motivo vira pretensão resistida) e (ii) obter as cédulas que o produtor
não tem. Sem ela, a inicial de prorrogação fica mais fraca.

Duas versões:
1. **Curta — pedido de documentos**: quando o produtor não tem as cédulas. Pede cópia integral de
   todas as cédulas e contratos rurais (custeio, investimento, comercialização, CPR, CCB de
   destinação rural), aditivos, termos de prorrogação/renegociação, extratos da conta vinculada e
   memória de cálculo do saldo, por e-mail em PDF.
2. **Longa — pedido de prorrogação**:
   - NOTIFICANTE (produtor, qualificação) / NOTIFICADO (banco/cooperativa, CNPJ, agência) /
     ASSUNTO: PEDIDO DE PRORROGAÇÃO DE DÍVIDA RURAL;
   - quadro das operações (uma por parágrafo: nº, tipo, finalidade, fonte de recursos, valor,
     saldo, vencimentos, garantias, avalistas);
   - DOS FATOS: atividade, área, safra(s) afetada(s), evento adverso com período, produção e
     receita projetadas x obtidas, decretos de emergência; laudo agronômico e laudo de capacidade
     de pagamento anexos;
   - DO DIREITO: MCR 2-6-4 (redação conferida no DNA 6.1, com a ressalva da Res. CMN 5.314/2026),
     Súmula 298/STJ, Lei 4.829/65 (arts. 1º, 2º, 3º, III, 14), Lei 8.171/91, art. 50, V;
   - DOS PEDIDOS: prorrogação com os mesmos encargos, carência e número de parcelas **iguais aos do
     laudo de capacidade de pagamento**; resposta por escrito e **motivada** em `[PREENCHER: prazo,
     sugestão 10 dias]`; suspensão de débito automático das parcelas discutidas; não negativação
     enquanto o pedido é analisado; envio das cédulas; comunicação só pelos advogados.
- Antes de redigir, confira: próximo vencimento (quanto mais antes do vencimento, melhor), canal
  oficial da agência (e-mail/protocolo), se a operação já foi prorrogada antes, se há
  renegociação oferecida pelo banco, se há execução ou negativação em curso.
- Não é peça processual: sem "Vossa Excelência"; tratamento "Prezados Senhores". Fecho
  "Atenciosamente," + cidade/data + assinatura do DNA.
- Sempre `STATUS: AGUARDA REVISÃO DO DR. DANIEL` (o envio é decisão dele).

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
