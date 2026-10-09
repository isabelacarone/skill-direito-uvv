---
phase: 02-formatar-elementos
plan: 02
subsystem: skill
tags: [abnt, referencias, modo-formatar, lista]
requires:
  - phase: 02-formatar-elementos
    provides: fluxo do modo Formatar, checar_skill.py estendido a tests/formatar
provides:
  - Modelos REF-48 a REF-64 em referencias-direito.md (13 tipos de obra, lista, normalizacao, meses)
  - tests/formatar caso-03 (lista de sete obras) e caso-04 (dado faltante)
affects: [02-03, 02-04]
tech-stack:
  added: []
  patterns: ["molde entre crases + Obrigatorios + origem copiada das linhas REF existentes"]
key-files:
  created:
    - tests/formatar/caso-03-lista-referencias.md
    - tests/formatar/caso-04-referencia-sem-dados.md
  modified:
    - .claude/skills/abnt-uvv-direito/references/referencias-direito.md
key-decisions:
  - "Meses abreviados completos entram com origem NBR 6023:2020 (o manual nao traz a tabela)"
  - "Linha Modelo lista copia as origens de REF-01, REF-06 e REF-07"
requirements-completed: [FMT-02, FMT-06]
duration: 15min
completed: 2026-10-09
---

# Phase 2 Plan 2: Referencias e lista no modo Formatar Summary

**A skill gera referencia de livro, capitulo, artigo, trabalho academico, site, evento e entrevista e monta a lista ordenada (esquerda, simples, 12 pt), pedindo editora, ano e data de acesso quando faltam.**

## Tasks

1. Task 1: `fbfc442` REF-48 a REF-64 (13 modelos por tipo, `Modelo lista`, normalizacao de link e data, meses); frase do cabecalho que remetia a "Fase 2" trocada.
2. Task 2: `39d819e` caso-03 (sete obras embaralhadas, ordem ALVES a YOSHIDA, `Ajustes nos dados:`) e caso-04 (livro sem editora e ano, site sem data de acesso).

## Verificacao

`checar_references.py` 220 regras 0 erros; `checar_skill.py` skill ok. Linhas REF-01 a REF-47 inalteradas (diff so troca a frase do cabecalho).

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None.

## Self-Check: PASSED
