---
phase: 03-checar-documento
plan: 01
subsystem: skill
tags: [abnt, docx, python-docx, verificador, modo-checar]
requires:
  - phase: 01-revisar-trechos
    provides: references/formatacao-grafica.md e citacoes.md com IDs e origens
provides:
  - scripts/verificar_docx.py (verificar, formatar, origem, LIMIARES, partes_do_documento)
  - Relatorio Markdown com checks, regra e origem lidas de references/
  - Fixtures ficticias tests/checar (caso-01 margem e fonte, caso-03 conforme)
affects: [03-02, 03-03]
tech-stack:
  added: []
  patterns: ["origem lida de references/ em tempo de execucao", "LIMIARES por ID conferidos contra o texto da regra pelo unittest"]
key-files:
  created:
    - .claude/skills/abnt-uvv-direito/scripts/verificar_docx.py
    - tests/checar/gerar_fixtures.py
    - tests/checar/caso-01-margem-fonte.docx
    - tests/checar/caso-03-conforme.docx
    - tools/tests/test_verificar_docx.py
  modified: []
key-decisions:
  - "Heranca de fonte/tamanho/entrelinhas/alinhamento resolvida por XML (run, estilo, base_style, docDefaults, tema)"
  - "Item que nao se resolve vai para Verificar manualmente, nunca vira check"
requirements-completed: [DOC-01, DOC-03]
duration: 25min
completed: 2026-10-09
---

# Phase 3 Plan 1: Verificador grafico do docx Summary

**`verificar_docx.py` relata fonte, tamanho, entrelinhas, alinhamento e margens de um .docx com check/cross, ID da regra e origem lida de references/; o caso 7 do briefing (2,5 cm e Times New Roman) sai com cross em GRA-09 e GRA-03 e o documento conforme sai sem nenhum.**

## Tasks

1. Task 1: `05abb66` fixtures ficticias e testes (RED: script ausente).
2. Task 2: `40a9f8d` nucleo: origem/bloco_regra, LIMIARES, abertura segura (so .docx, zip, ate 50 MB), heranca de propriedades.
3. Task 3: `231bffa` titulos, corpo, citacoes/legendas excluidas, cinco itens, `verificar`, `formatar`, codigos de saida 0/1/2.

## Verificacao

`python -m unittest discover -s tools/tests` OK (31 testes); CLI caso-01 sai 1 com GRA-09 e GRA-03; caso-03 sai 0; `checar_references.py` 243 regras, 0 erros; grep de `.save(`/subprocess/rede = 0; .docx commitados nao mudam apos os testes.

## Deviations from Plan

**1. [Rule 1 - Plano x realidade] Criterio "grep -c ✘ = 0" no caso conforme**
- **Issue:** P-18 manda a linha final `Resumo: N ✔, M ✘, K ...`, que contem `0 ✘` mesmo sem reprovacao; o criterio literal (e o assertNotIn do teste) contradiz o formato.
- **Fix:** o teste e a conferencia excluem a linha `Resumo:`; o teste confere tambem `Resumo: 5 ✔, 0 ✘, 0 verificar manualmente`. Nenhuma linha de item tem ✘.
- **Commit:** 231bffa

## Known Stubs

None.

## Self-Check: PASSED
