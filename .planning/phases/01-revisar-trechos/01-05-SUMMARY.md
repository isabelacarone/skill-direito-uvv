---
phase: 01-revisar-trechos
plan: 05
subsystem: skill
tags: [skill, abnt, revisar, python, tests]

requires:
  - phase: 01-01
    provides: "checar_references.py, manual_mapa.json"
  - phase: 01-02
    provides: "formatacao-grafica.md, pre-textuais.md"
  - phase: 01-03
    provides: "citacoes.md, tabelas-ilustracoes.md"
  - phase: 01-04
    provides: "referencias-direito.md, regras-curso-direito.md"
provides:
  - "SKILL.md abnt-uvv-direito (83 linhas): precedencia, roteamento para references/, regua do parecer, formato de saida, guardrails"
  - "tools/checar_skill.py com --autoteste"
  - "tests/revisar/: 6 casos com entrada, esperado e nao-pode"
affects: [fase-2]

key-files:
  created:
    - .claude/skills/abnt-uvv-direito/SKILL.md
    - tools/checar_skill.py
    - tests/revisar/caso-01-citacao-longa.md
    - tests/revisar/caso-02-apud-invertido.md
    - tests/revisar/caso-03-afirmacao-sem-fonte.md
    - tests/revisar/caso-04-sem-secao.md
    - tests/revisar/caso-05-fora-do-manual.md
    - tests/revisar/caso-06-primeira-pessoa.md

key-decisions:
  - "Regua: Critico = falha de fundamentacao/citacao (a); Ajustes necessarios = formato (b) ou ajuste fino (c); Conforme = nenhuma"
  - "caso-01 fixado em Ajustes necessarios (citacao com fonte e pagina, defeito so de formato); caso-06 em Ajustes necessarios"
  - "caso-05 usa pergunta sobre citar texto de IA, provada ausente do manual (grep = 0)"

requirements-completed: [BASE-01, BASE-04, REV-01, REV-02, REV-03, REV-04, QA-02]

duration: 25min
completed: 2026-10-09
---

# Phase 1 Plan 05: SKILL.md do modo Revisar Summary

**SKILL.md curto (83 linhas) que roteia para os 6 arquivos de references/, devolve parecer Conforme/Ajustes necessarios/Critico com tabela de inconformidades de origem copiada, mais verificador estrutural e 6 casos aprovados pela autora.**

## Task Commits
1. Task 1 SKILL.md: 914fa78
2. Task 2 checar_skill.py + 6 casos: 533ada8
3. Task 3 checkpoint: autora aprovou os 6 casos numa sessao nova ("APROVADO").

## Deviations from Plan
None - plan executed exactly as written.

## Known Stubs
None.

## Self-Check: PASSED
- `python tools/checar_skill.py` -> skill ok; `--autoteste` ok; unittest OK.
