---
name: revisao-controladoria
description: "Revisão final da controladoria: confere a peça contra o DNA (nicho agro, CPC), os autos e as regras e devolve o parecer com STATUS."
---

# revisao-controladoria

Confira:
- formatação e estrutura do DNA (a formatação é provisória, mas é a vigente);
- justiça e endereçamento certos (Estadual x Federal, DNA 3.1) e abertura, fecho e assinatura;
- quadro das operações batendo com as cédulas e extratos (nº, taxa, saldo, vencimentos);
- cada pedido com fato, fundamento e valor; aritmética e valor da causa;
- prazo e termo inicial (dias úteis, art. 219; juntada do mandado/AR quando for o caso, art. 231);
- jurisprudência só verificada: todo precedente fora do DNA como [CONFERIDO] tem de estar marcado
  [CONFERIR PRECEDENTE]; nenhum número de processo, relator ou data inventado;
- MCR transcrito só com a redação conferida e vigente (alerta Res. CMN 5.314/2026);
- nenhum [PREENCHER] esquecido;
- coerência com a decisão ou com a defesa rebatida.

Entregue `saida/PARECER_REVISAO.md` com uma linha exatamente em um destes formatos:
`STATUS: APROVADA` | `STATUS: APROVADA COM RESSALVAS` | `STATUS: NÃO APROVADA`
seguida dos achados, classificados como crítico, ajuste ou sugestão. Se houver ressalvas, aplique-as
e diga o que mudou.

Leia antes o `SISTEMA/backend/app/juridico/DNA_ESCRITORIO.md`.
