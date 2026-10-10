# Caso 03 - documento sem ✘

## Entrada

Pedido: "Cheque a formatação de tests/checar/caso-03-conforme.docx"

## Esperado

- A skill roda `python .claude/skills/abnt-uvv-direito/scripts/verificar_docx.py tests/checar/caso-03-conforme.docx` e entrega o relatório como veio, sem trocar resultado nem origem:

```
# Relatório de formatação: caso-03-conforme.docx

| # | Item | Resultado | Regra | Detalhe |
|---|---|---|---|---|
| 1 | Fonte do corpo do texto (Arial) | ✔ | GRA-03 (Manual 3.1, p. 32) | 9 parágrafos conferidos |
| 2 | Tamanho da fonte do corpo do texto (12 pt) | ✔ | GRA-03 (Manual 3.1, p. 32) | 9 parágrafos conferidos |
| 3 | Entrelinhas do corpo do texto (1,5) | ✔ | GRA-05 (Manual 3.2, p. 32) | 5 parágrafos conferidos |
| 4 | Alinhamento do corpo do texto (justificado) | ✔ | GRA-05 (Manual 3.2, p. 32) | 5 parágrafos conferidos |
| 5 | Margens (3/3/2/2 cm) | ✔ | GRA-09 (Manual 3.2, p. 32) | 1 seção(ões) conferida(s) |
| 6 | Recuo da citação longa (4 cm) | ✔ | CIT-06 (Manual 4.1.3, p. 37) | 1 parágrafos conferidos |
| 7 | Fonte da citação longa (Arial 10) | ✔ | CIT-06 (Manual 4.1.3, p. 37) | 1 parágrafos conferidos |
| 8 | Entrelinhas da citação longa (simples) | ✔ | CIT-06 (Manual 4.1.3, p. 37) | 1 parágrafos conferidos |
| 9 | Citação longa sem aspas | ✔ | CIT-06 (Manual 4.1.3, p. 37) | 1 parágrafos conferidos |
| 10 | Numeração de página no cabeçalho | ✔ | GRA-12 (Manual 3.3, p. 33) | campo de página em 1 cabeçalho(s) |
| 11 | Número alinhado à direita | ✔ | GRA-12 (Manual 3.3, p. 33) | 1 campo(s) conferido(s) |
| 12 | Fonte do número (Arial 10) | ✔ | GRA-13 (Manual 3.1, p. 32) | Arial 10 pt |
| 13 | Algarismos arábicos | ✔ | GRA-12 (Manual 3.3, p. 33) | formato decimal na seção do corpo |
| 14 | Seção primária em página nova | ✔ | GRA-16 (Manual 3.4, p. 34) | 2 seções primárias conferidas |
| 15 | Seção primária em negrito, caixa alta e à esquerda | ✔ | GRA-16 (Manual 3.4, p. 34) | 2 parágrafos conferidos |
| 16 | Grafia dos títulos por nível | ✔ | GRA-18 (Manual 3.4, p. 34) | 2 parágrafos conferidos |
| 17 | Numeração consecutiva das seções | ✔ | GRA-15 (Manual 3.4, p. 33) | 4 títulos numerados em sequência |

## Verificar manualmente

- Extensão da citação (até 10 linhas): o limite de 10 linhas depende da paginação do Word: conferir à mão — CIT-07 (Regra do curso (Projeto de Pesquisa, Orientações Gerais))
- Citação longa sem recuo: citação longa sem recuo e sem aspas não é identificável pelo arquivo; nenhum trecho entre aspas com mais de 225 caracteres no corpo (estimativa de apoio do SKILL.md, não regra do manual) — CIT-06 (Manual 4.1.3, p. 37)
- Início da numeração (primeira folha de texto): a contagem parte da folha de rosto e o número aparece a partir da primeira folha de texto; em que folha isso ocorre depende de seções e da paginação: conferir à mão — GRA-11 (Manual 3.3, p. 33); GRA-12 (Manual 3.3, p. 33)

Resumo: 17 ✔, 0 ✘, 3 verificar manualmente
```

- Diz que nenhum item automático foi reprovado e que os itens de "Verificar manualmente" ainda precisam de conferência no Word.
- Sem `Como corrigir:`, pois não há ✘.
- Oferece o modo Revisar para o conteúdo.

## Não pode

- Declarar o documento "aprovado" ou "conforme ao manual" sem os itens de verificação manual.
- Trocar "verificar manualmente" por ✔.
