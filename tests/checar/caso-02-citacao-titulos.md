# Caso 02 - citação longa, numeração e títulos fora do padrão

## Entrada

Pedido: "Cheque a formatação de tests/checar/caso-02-citacao-titulos.docx"

## Esperado

- A skill roda `python .claude/skills/abnt-uvv-direito/scripts/verificar_docx.py tests/checar/caso-02-citacao-titulos.docx` e entrega o relatório como veio, sem trocar resultado nem origem:

```
# Relatório de formatação: caso-02-citacao-titulos.docx

| # | Item | Resultado | Regra | Detalhe |
|---|---|---|---|---|
| 1 | Fonte do corpo do texto (Arial) | ✔ | GRA-03 (Manual 3.1, p. 32) | 10 parágrafos conferidos |
| 2 | Tamanho da fonte do corpo do texto (12 pt) | ✔ | GRA-03 (Manual 3.1, p. 32) | 10 parágrafos conferidos |
| 3 | Entrelinhas do corpo do texto (1,5) | ✔ | GRA-05 (Manual 3.2, p. 32) | 6 parágrafos conferidos |
| 4 | Alinhamento do corpo do texto (justificado) | ✔ | GRA-05 (Manual 3.2, p. 32) | 6 parágrafos conferidos |
| 5 | Margens (3/3/2/2 cm) | ✔ | GRA-09 (Manual 3.2, p. 32) | 1 seção(ões) conferida(s) |
| 6 | Recuo da citação longa (4 cm) | ✘ | CIT-06 (Manual 4.1.3, p. 37) | 1 de 1 parágrafos: §13 '“Esta citacao longa e inteiramente ficti…' (recuo 2,0 cm) |
| 7 | Fonte da citação longa (Arial 10) | ✘ | CIT-06 (Manual 4.1.3, p. 37) | 1 de 1 parágrafos: §13 '“Esta citacao longa e inteiramente ficti…' (Arial 12,0 pt) |
| 8 | Entrelinhas da citação longa (simples) | ✘ | CIT-06 (Manual 4.1.3, p. 37) | 1 de 1 parágrafos: §13 '“Esta citacao longa e inteiramente ficti…' (entrelinhas 1,5) |
| 9 | Citação longa sem aspas | ✘ | CIT-06 (Manual 4.1.3, p. 37) | 1 de 1 parágrafos: §13 '“Esta citacao longa e inteiramente ficti…' (com aspas) |
| 10 | Numeração de página no cabeçalho | ✘ | GRA-12 (Manual 3.3, p. 33) | campo de página no rodapé; a regra pede o cabeçalho |
| 11 | Número alinhado à direita | ✘ | GRA-12 (Manual 3.3, p. 33) | número centralizado (esperado: canto superior direito) |
| 12 | Fonte do número (Arial 10) | ✘ | GRA-13 (Manual 3.1, p. 32) | número em Arial 12,0 pt (esperado: Arial 10 pt) |
| 13 | Algarismos arábicos | ✔ | GRA-12 (Manual 3.3, p. 33) | formato decimal na seção do corpo |
| 14 | Seção primária em página nova | ✘ | GRA-16 (Manual 3.4, p. 34) | 1 de 2 seções primárias: sem quebra de página antes de: 2 SEGUNDA SEÇÃO DE TESTE (se o título já cai no topo por acaso, insira a quebra mesmo assim) |
| 15 | Seção primária em negrito, caixa alta e à esquerda | ✔ | GRA-16 (Manual 3.4, p. 34) | 2 parágrafos conferidos |
| 16 | Grafia dos títulos por nível | ✘ | GRA-18 (Manual 3.4, p. 34) | 1 de 2 parágrafos: §9 '1.1 Seção secundária de teste' (nível 2: esperado maiúsculas sem negrito) |
| 17 | Numeração consecutiva das seções | ✘ | GRA-15 (Manual 3.4, p. 33) | saltos: 1.1.2 (esperado 1.1.1) |

## Verificar manualmente

- Extensão da citação (até 10 linhas): o limite de 10 linhas depende da paginação do Word: conferir à mão — CIT-07 (Regra do curso (Projeto de Pesquisa, Orientações Gerais))
- Citação longa sem recuo: parágrafos do corpo com trecho entre aspas de mais de 225 caracteres: §12. É estimativa de apoio do SKILL.md, não regra do manual; confirmar se é citação direta longa sem recuo — CIT-06 (Manual 4.1.3, p. 37)
- Início da numeração (primeira folha de texto): a contagem parte da folha de rosto e o número aparece a partir da primeira folha de texto; em que folha isso ocorre depende de seções e da paginação: conferir à mão — GRA-11 (Manual 3.3, p. 33); GRA-12 (Manual 3.3, p. 33)

Resumo: 7 ✔, 10 ✘, 3 verificar manualmente
```

- Abaixo do relatório, `Como corrigir:` com uma linha por ✘:
  - citação longa: recuo de 4 cm, Arial 10, entrelinhas simples e sem aspas (CIT-06, Manual 4.1.3, p. 37);
  - numeração de página: no cabeçalho, à direita, em Arial 10 (GRA-12, Manual 3.3, p. 33; GRA-13, Manual 3.1, p. 32);
  - seção primária: quebra de página antes de "2 SEGUNDA SEÇÃO DE TESTE" (GRA-16, Manual 3.4, p. 34);
  - título 1.1 em maiúsculas, sem negrito (GRA-18, Manual 3.4, p. 34);
  - renumerar 1.1.2 para 1.1.1 (GRA-15, Manual 3.4, p. 33).
- O limite de 10 linhas da citação continua em "Verificar manualmente".

## Não pode

- Dar ✔ ou ✘ para o limite de 10 linhas da citação.
- Tratar a margem como errada: ela está conforme.
- Acrescentar item que o script não relatou.
