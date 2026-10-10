---
phase: 03-checar-documento
plan: 03
subsystem: skill
tags: [abnt, docx, modo-checar, skill, verificador, casos]
requires:
  - phase: 03-checar-documento
    provides: verificar_docx.py completo (03-01 e 03-02) e fixtures tests/checar
provides:
  - "## Fluxo do modo Checar documento no SKILL.md"
  - checar_skill.py cobrindo o modo (CASOS_CHECAR, MIN_CHECAR)
  - 4 casos em tests/checar com a saida real do script
affects: []
tech-stack:
  added: []
  patterns: ["relatorio do script entregue como veio, com Como corrigir: so por cima", "secoes de caso conferidas fora de blocos cercados"]
key-files:
  created:
    - tests/checar/caso-01-margem-fonte.md
    - tests/checar/caso-02-citacao-titulos.md
    - tests/checar/caso-03-conforme.md
    - tests/checar/caso-04-arquivo-inexistente.md
  modified:
    - tools/checar_skill.py
    - .claude/skills/abnt-uvv-direito/SKILL.md
key-decisions:
  - "SKILL.md sem o texto que tratava o script como possivelmente ausente; sem python ou python-docx, pede o trecho para o modo Revisar"
requirements-completed: [DOC-01, DOC-02, DOC-03]
duration: 40min
completed: 2026-10-09
---

# Phase 3 Plan 3: Fluxo Checar documento Summary

**A skill passa a rodar `verificar_docx.py` num .docx apontado pela autora e entregar o relatorio sem reescrever resultado nem origem; `checar_skill.py` cobre o modo e 4 casos fixam a saida esperada. A autora rodou os casos numa sessao nova e aprovou.**

## Tasks

1. Task 1 RED: `c10e74d` defeitos novos no autoteste (falhou como esperado).
2. Task 1 GREEN: `aff84e9` regras de P-31 em `checar` e tres strings em `OBRIGATORIAS`.
3. Task 2: `203f030` fluxo no SKILL.md (100 linhas) e casos 01 a 04.
4. Task 3: checkpoint humano, aprovado pela autora ("Aprovado").

## Verificacao

`checar_skill.py` skill ok; `--autoteste` ok; `checar_references.py` 243 regras, 0 erros; unittest 50 testes OK; nenhum nome real em tests/checar; nenhum .docx novo fora de tests/checar.

## Deviations from Plan

**1. [Rule 1 - Plano x realidade] Criterio `grep -c "## Fluxo do modo Checar documento" = 1`**
- **Issue:** P-30 exige duas referencias a esse titulo (fluxo Revisar e "Pedidos fora"), logo o grep devolve 3.
- **Fix:** a secao existe uma vez; texto aplicado como no plano.
- **Commit:** 203f030

**2. [Rule 1 - Plano x realidade] RED**
- **Issue:** o defeito "existir na skill" ja gera erro no RED, pois `PROIBIDAS_SKILL` e estendida nele conforme o plano.
- **Commit:** c10e74d

**3. Observacao:** a linha 118 de `tools/checar_skill.py` tem uma tabulacao literal em `[ \t]*$`; funciona e foi mantida.

## Known Stubs

None.

## Threat Flags

None. Nenhum .docx real nem trecho real entrou no repositorio (T-03-10).

## Self-Check: PASSED
