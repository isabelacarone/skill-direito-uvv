---
phase: 04-valida-o
plan: 01
subsystem: validacao
tags: [casos, rastreabilidade, abnt, qa]
requires: []
provides:
  - tests/validacao/RASTREABILIDADE.md (mapa dos 8 casos do briefing)
  - tests/validacao/RESULTADOS.md (8 casos pendentes)
affects: [04-02]
key-files:
  created:
    - tests/validacao/RASTREABILIDADE.md
    - tests/validacao/RESULTADOS.md
  modified:
    - tests/revisar/caso-01-citacao-longa.md
    - tests/revisar/caso-02-apud-invertido.md
    - tools/checar_skill.py
key-decisions:
  - "Caso errado, regra certa: casos 1 e 2 corrigidos; references/ intocado"
requirements-completed: [QA-01]
completed: 2026-10-09
---

# Phase 4 Plan 1: Rastreabilidade e casos corrigidos Summary

**Os 8 casos do briefing apontam para casos fixos existentes (sem duplicar), os casos 1 e 2 deixam de contradizer CIT-19 e CIT-16, e o registro de resultados nasce todo `pendente`.**

## Tasks

1. Task 1: `b30153e` caso-01 com `(Streck, 2017, p. 25)` e nova linha em Não pode; caso-02 com `Segundo Freire (1994 apud Streck, 2017, p. 25)`; regex de checar_skill.py com `\t`.
2. Task 2: `86823fa` RASTREABILIDADE.md (8 linhas) e RESULTADOS.md (8 `pendente`).

## Conferência no PDF

- Página 41 (4.4.2): "Quando for pessoa física a indicação deve ser feita pelo sobrenome do autor, em letras maiúsculas e minúsculas".
- Página 40 (4.3): "Os elementos devem ser indicados na seguinte ordem: autoria ou a primeira palavra do título; data; página do documento original, se houver; a expressão apud; autoria ...; data; página da fonte consultada, se houver." Exemplo 3 da mesma página: `(Boss e Krauss, 2007 apud Bender, 2014)`, compatível com a forma `1994 apud Streck, 2017, p. 25`.
- Página 39 traz a definição de citação de citação (4.3).

## Verificação

`checar_skill.py` skill ok; `--autoteste` ok; `checar_references.py` 243 regras, 0 erros; unittest 50 testes OK. Grep de chamadas de pessoa física em caixa alta nos casos: nenhuma ocorrência. `grep -cP "\t"` em checar_skill.py = 0. `| passou |` em RESULTADOS.md = 0.

## Deviations from Plan

**1. [Rule 1 - Plano x realidade] Contagem dos "outros casos fixos"**
- Os 6 casos de tests/revisar estão todos mapeados, então os 12 restantes são 9 em tests/formatar e 3 em tests/checar; listados assim em RASTREABILIDADE.md.

**2. Observação:** o comando `unittest ... | tail -1` mostra ruído de saída de teste (`2 regras, 1 erros`) após o `OK`; é saída esperada de um teste de erro, não falha (50 testes OK).

## Known Stubs

None.

## Threat Flags

None.

## Self-Check: PASSED
