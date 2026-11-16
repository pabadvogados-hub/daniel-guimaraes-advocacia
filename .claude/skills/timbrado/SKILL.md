---
name: timbrado
description: Coloca qualquer texto de peça no papel timbrado do escritório (Century Gothic 12, recuo de 3 cm, títulos em caixa alta e negrito).
---

# timbrado

Use SEMPRE no último passo de qualquer peça. Nunca recrie o cabeçalho: o modelo oficial é
`SISTEMA/backend/app/juridico/modelos/TIMBRADO.docx`.

A formatação (fonte, recuo, títulos) é a PROVISÓRIA do DNA, herdada da base, até lermos 5 a 10
peças reais do Dr. Daniel; depois ajuste `ESC_FONTE_PECA`, `ESC_TAMANHO_PECA` e
`ESC_RECUO_PECA_CM` no servidor e troque o TIMBRADO.docx pelo do escritório.

Como usar:
```
python .claude/skills/timbrado/montar_peca.py --texto PECA.txt --saida "PECA.docx"
```
O texto vai com um parágrafo por linha e sem markdown. O script reconhece sozinho:
- endereçamento, "Processo nº", RECORRENTE/RECORRIDA/ORIGEM e o fecho: ficam sem recuo
  (APELANTE/APELADO/AGRAVANTE em caixa alta saem como título: negrito e sem recuo);
- título (linha toda em caixa alta): negrito e sem recuo;
- linha que termina em OAB/UF nº: assinatura centralizada em negrito;
- "Cidade, dd de mês de aaaa.": alinhada à direita;
- o restante: justificado, com recuo de 3 cm na primeira linha.

