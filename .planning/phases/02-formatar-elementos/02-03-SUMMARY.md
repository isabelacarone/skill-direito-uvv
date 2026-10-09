---
phase: 02-formatar-elementos
plan: 03
subsystem: skill
tags: [abnt, legislacao, jurisprudencia, legendas, modo-formatar]
requires:
  - phase: 02-formatar-elementos
    provides: modelos REF-48 a REF-64, checar_skill.py estendido a tests/formatar
provides:
  - Modelos REF-65 a REF-74 (Constituicao, lei, acordao, sumula, atos normativos, citacao de lei)
  - Modelos TAB-21 a TAB-26 (titulo de tabela e ilustracao, fonte, formatacao, tabela em varias paginas)
  - tests/formatar caso-05, caso-06, caso-07 e caso-10
affects: [02-04]
tech-stack:
  added: []
  patterns: ["molde entre crases + Obrigatorios + origem copiada das linhas REF/TAB"]
key-files:
  created:
    - tests/formatar/caso-05-lei-acordao-soltos.md
    - tests/formatar/caso-06-legendas.md
    - tests/formatar/caso-07-lista-com-legislacao.md
    - tests/formatar/caso-10-sumula-ato-normativo.md
  modified:
    - .claude/skills/abnt-uvv-direito/references/referencias-direito.md
    - .claude/skills/abnt-uvv-direito/references/tabelas-ilustracoes.md
key-decisions:
  - "Acordao sem relator ou data: pergunta unica, nunca inventa (P-12)"
  - "Titulo de legenda sem ponto final, Fonte com ponto (P-18)"
requirements-completed: [FMT-03, FMT-04, FMT-06]
duration: 12min
completed: 2026-10-09
---

# Phase 2 Plan 3: Legislacao, jurisprudencia e legendas Summary

**A skill gera referencia de Constituicao, lei, acordao, sumula e ato normativo, e legendas de tabela, figura e quadro com Fonte, pedindo relator, data ou autoria quando faltam.**

## Tasks

1. Task 1: `6edc6c4` REF-65 a REF-74 e casos 05 (lei e acordao do STF soltos, pergunta unica sobre relator e data), 07 (lista mista BRASIL, CUNHA, CURITIBA, FREYRE, REGO) e 10 (sumula, deliberacao, oficio sem ementa).
2. Task 2: `0ad44a1` TAB-21 a TAB-26 e caso-06 (tabela de terceiro, quadro proprio, figura sem autoria perguntada); frase do cabecalho que remetia a geracao de texto trocada.

## Verificacao

`checar_references.py` 236 regras 0 erros; `checar_skill.py` skill ok; 8 casos em tests/formatar. Criterios de aceite por grep conferidos.

## Deviations from Plan

None - plan executed exactly as written. Os IDs novos seguiram a numeracao livre (REF-65+, TAB-21+).

## Known Stubs

None.

## Self-Check: PASSED
