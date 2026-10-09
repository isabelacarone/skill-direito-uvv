---
phase: 02-formatar-elementos
plan: 01
subsystem: skill
tags: [abnt, citacoes, modo-formatar, verificador]
requires:
  - phase: 01-revisar-trechos
    provides: references/ com regras e origens, checar_skill.py, casos de tests/revisar
provides:
  - Fluxo do modo Formatar no SKILL.md (dado faltante, saida com Regra aplicada)
  - Modelos de citacao CIT-43 a CIT-49 em citacoes.md
  - tests/formatar caso-01 e caso-02
  - checar_skill.py estendido a tests/formatar
affects: [02-02, 02-03, 02-04]
tech-stack:
  added: []
  patterns: ["linha de modelo no contrato de checar_references.py", "origem de caso copiada de references/"]
key-files:
  created:
    - tests/formatar/caso-01-citacoes.md
    - tests/formatar/caso-02-citacao-sem-pagina.md
  modified:
    - tools/checar_skill.py
    - .claude/skills/abnt-uvv-direito/SKILL.md
    - .claude/skills/abnt-uvv-direito/references/citacoes.md
key-decisions:
  - "Caso longo usa o exemplo do Manual 4.1.3, p. 37 (Franca, 2003, p. 30), conferido na pagina renderizada"
  - "Estimativa de linhas (225 e 650 caracteres) fica no SKILL.md como apoio, declarada como nao regra do manual"
requirements-completed: [FMT-01, FMT-06]
duration: 20min
completed: 2026-10-09
---

# Phase 2 Plan 1: Citacoes no modo Formatar Summary

**A skill gera citacao direta curta, longa, indireta e apud com `Regra aplicada:` copiada de citacoes.md, e pede a pagina quando falta; verificador cobre tests/formatar.**

## Tasks

1. Task 1 (TDD): RED `4b3f2f2` (autoteste com 9 defeitos novos, falhando pelos motivos certos), GREEN `6342bf3` (checagens de caso, origem, `< >`, data de acesso, Fase 2, fluxo).
2. Task 2: `b31b494` SKILL.md (secao Fluxo do modo Formatar, 91 linhas), CIT-43 a CIT-49, caso-01 e caso-02.

## Verificacao

`checar_references.py` 203 regras 0 erros; `checar_skill.py` skill ok; `--autoteste` ok; unittest 19 OK.

## Deviations from Plan

**1. [Rule 1 - Bug] Origem fabricada do autoteste**
- **Found during:** Task 1
- **Issue:** o plano usa `Manual 4.1.3, p. 37` como origem fabricada, mas CIT-06 ja contem essa origem, entao o defeito nunca geraria erro.
- **Fix:** usada `Manual 4.1.2, p. 37` (valida no mapa, ausente de references/).
- **Commit:** 4b3f2f2

O RED termina com "autoteste falhou" (esperado); "autoteste ok" so vale apos a Task 1 GREEN, apesar do criterio de aceitacao do plano sugerir o contrario.

## Known Stubs

None.

## Self-Check: PASSED
