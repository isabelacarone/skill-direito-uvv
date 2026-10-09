---
phase: 01-revisar-trechos
plan: 02
subsystem: references
tags: [abnt, manual-uvv, references, markdown]

requires:
  - phase: 01-01
    provides: "manual_mapa.json, checar_references.py, manual_paginas.py, extrair_docx.py"
provides:
  - "references/formatacao-grafica.md: 22 regras GRA (manual cap. 3, p. 32-35)"
  - "references/pre-textuais.md: 34 regras PRE (manual 2.1, 2.2, Anexo A p. 71, mais regras do Projeto de Pesquisa)"
affects: [01-03, 01-04, 01-05]

key-files:
  created:
    - .claude/skills/abnt-uvv-direito/references/formatacao-grafica.md
    - .claude/skills/abnt-uvv-direito/references/pre-textuais.md

key-decisions:
  - "Ficha catalografica (2.1.3) omitida por decisao da autora, inclusive na ordem dos elementos (p. 71 a mostra no diagrama)"
  - "Cinco niveis de titulo gravados a partir do exemplo renderizado da p. 34 (o texto so diz 'maiuscula, negrito, italico...')"

requirements-completed: [BASE-02]

duration: 20min
completed: 2026-10-09
---

# Phase 1 Plan 02: formatacao-grafica e pre-textuais Summary

**56 regras condensadas (22 GRA + 34 PRE), cada uma com item e pagina impressa conferidos na pagina renderizada, validadas por checar_references.py (0 erros).**

## Paginas impressas renderizadas e conferidas
- formatacao-grafica.md: 32, 33, 34, 35
- pre-textuais.md: 8, 10, 12, 14, 18, 20, 21, 24, 26, 27, 71 (visualizadas); 9, 11, 13, 15-17, 19, 22, 23, 25 (so figuras-modelo, renderizadas mas nao usadas como fonte de regra)

## Task Commits
1. Task 1 formatacao-grafica.md: 19f875d
2. Task 2 pre-textuais.md: b77034d

## Deviations from Plan

### Divergencias registradas
- **Grafia dos niveis de titulo:** o plano e o briefing listam maiusculas+negrito / maiusculas / negrito / normal / italico; a p. 34 renderizada confirma exatamente isso no exemplo (o texto da regra e generico). Gravado conforme a renderizacao (GRA-18).
- **Margem verso/anverso:** texto cita "Figura 13", modelo e a Figura 14 (p. 33); registrado como Nota em GRA-10.
- **Briefing x manual:** o briefing chama o cap. 3 de "4.1"; usado o item do manual (3.1 a 3.6). Nenhuma divergencia de pagina encontrada.
- **Paginacao em Arial 10 (GRA-13):** vem de 3.1 (p. 32), nao de 3.3; origem gravada em 3.1.
- **Criterio "4 cm":** nenhuma regra com 4 cm foi gravada (recuo da citacao longa e do cap. 4, fora deste plano); GRA-04 aponta so por referencia cruzada a citacoes.md, sem citar pagina nao vista.

Nenhum auto-fix de codigo.

## Known Stubs
None.

## Self-Check: PASSED
- Arquivos existem; commits 19f875d e b77034d presentes; verificador: 56 regras, 0 erros; "ficha catalogr" = 0 ocorrencias.
