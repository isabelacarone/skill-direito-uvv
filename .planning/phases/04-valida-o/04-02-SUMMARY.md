---
phase: 04-valida-o
plan: 02
subsystem: validacao
tags: [tdd, validacao, entrypoint, qa]
requires: [04-01]
provides:
  - tools/validar_tudo.py (entrypoint unico, portao --final)
affects: [04-03]
key-files:
  created:
    - tools/validar_tudo.py
    - tools/tests/test_validar_tudo.py
key-decisions:
  - "Portao --final testado so com copias temporarias de RESULTADOS.md"
requirements-completed: []
completed: 2026-10-09
---

# Phase 4 Plan 2: Entrypoint validar_tudo Summary

**`python tools/validar_tudo.py` roda os 4 verificadores, confere as tabelas de tests/validacao/, compara o relatorio real de verificar_docx.py com o bloco fixado em cada caso de tests/checar e imprime a tabela dos 8 casos; `--final` so sai 0 com os 8 `passou` datados.**

## Tasks

1. RED `7c6412e`: 20 testes em tools/tests/test_validar_tudo.py, falhando por ImportError de `validar_tudo`.
2. GREEN `6079d13`: tools/validar_tudo.py (biblioteca padrao). Unittest 70 testes OK.

## Verificacao

- `python tools/validar_tudo.py`: 4 verificadores ok, 8 casos com Automatico `ok` e Autora `pendente`, `validacao ok`, saida 0.
- `python tools/validar_tudo.py --final`: saida 1 (RESULTADOS.md real ainda `pendente`), como esperado ate o 04-03.
- Nenhum teste chama `rodar_verificadores` nem `--final` sem `--resultados`.

## Deviations from Plan

None - plano executado como escrito. Nenhum caso real divergiu do relatorio do script, entao nenhum caso nem script precisou de correcao.

Observacao: a saida do unittest dentro do verificador mostra `2 regras, 1 erros` (ruido de um teste de erro existente), nao e falha.

## Estado de QA-01

QA-01 permanece Pending: fecha so no 04-03, depois dos resultados da autora e do gate `--final`. RESULTADOS.md nao foi tocado.

## Known Stubs

None.

## Threat Flags

None.

## Self-Check: PASSED
