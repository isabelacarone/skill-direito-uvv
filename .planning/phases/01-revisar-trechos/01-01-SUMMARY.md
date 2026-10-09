---
phase: 01-revisar-trechos
plan: 01
subsystem: tooling
tags: [python, pdftotext, python-docx, unittest, abnt]

requires: []
provides:
  - "tools/manual_mapa.json: pagina impressa -> pagina PDF e item -> intervalo de paginas impressas do Manual UVV 2024"
  - "tools/checar_references.py: verificador do contrato de linha de regra de references/*.md"
  - "tools/extrair_docx.py: dump por paragrafo dos .docx do curso"
affects: [01-02, 01-03, 01-04, 01-05]

tech-stack:
  added: []
  patterns:
    - "Citacao 'Manual X.Y, p. N' conferida contra mapa gerado do PDF"
    - "TDD com unittest e arquivos temporarios"

key-files:
  created:
    - tools/manual_paginas.py
    - tools/manual_mapa.json
    - tools/extrair_docx.py
    - tools/checar_references.py
    - tools/tests/test_checar_references.py
  modified: []

key-decisions:
  - "Item 4.1.9 so existe no sumario do manual (indicador quebrado) e nao no corpo; fica fora de itens e listado em somente_sumario, entao citar 4.1.9 falha no verificador"
  - "Titulos de nivel 1 no corpo exigem texto em maiusculas, para nao confundir datas como '20 jun. 2019' com secoes"

requirements-completed: [BASE-02]

duration: 15min
completed: 2026-10-09
---

# Phase 1 Plan 01: Ferramentas de verificacao de paginas Summary

**Mapa pagina/item gerado do proprio PDF do manual, verificador de linhas de regra que reprova pagina inventada e extrator dos dois .docx do curso.**

## Accomplishments
- `manual_mapa.json` com 65 paginas impressas (PDF 8 a 72) e 114 itens; conferido: 4.1.3 em 37, 6.3.11 e 6.3.12 em 66, 3.2 em 32.
- `checar_references.py` valida ID/prefixo por arquivo, unicidade, origem obrigatoria, intervalo de paginas por item, `Regra do curso (...)`, NBR e `Decisao da autora` so combinada; sai com codigo 1 em erro.
- 19 testes unittest passando (RED commitado antes do GREEN).
- `extrair_docx.py` confirma "9 REFERÊNCIAS" e "Exemplo de Referências" no Projeto de Pesquisa e "FONTES INICIAIS" no Estudo Dirigido.

## Task Commits
1. Task 1 (mapa + extrator): b4306dd
2. Task 2 RED (testes): 3f09640
3. Task 2 GREEN (verificador): 4fc177e

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Falsos positivos de titulo no corpo**
- **Found during:** Task 1
- **Issue:** "20 jun. 2019" e "26 jun. 2019" (p. 59) eram lidos como secoes 20 e 26, quebrando a ordem e escondendo os itens 6.3.x.
- **Fix:** titulos sem ponto (nivel 1) exigem texto em maiusculas.
- **Files modified:** tools/manual_paginas.py
- **Commit:** b4306dd

**2. [Plan assumption incorrect] Item 4.1.9 nao existe no corpo**
- **Issue:** o criterio de aceite esperava 4.1.9 no mapa "pela varredura do corpo". O PDF so tem 4.1.9 no sumario (com "Erro! Indicador nao definido."); o corpo nao tem essa secao (4.1.8 vai direto para 4.2).
- **Fix:** nao inventar pagina; 4.1.9 fica na chave `somente_sumario` e o AVISO de stderr o relata. Citar 4.1.9 em references/ falha no verificador (teste incluso).
- **Commit:** b4306dd

**Total deviations:** 2. Impacto: nenhum no escopo; o criterio sobre 4.1.9 nao e atendido literalmente, de proposito (Core Value: nunca inventar pagina).

## Known Stubs
None.

## Notes
Avisos informativos de mapa (stderr): itens 2.1.8, 4.4.7, 4.4.10 a 4.4.14 e 6.3.2 estao no corpo mas ausentes do sumario; nenhuma divergencia de pagina entre corpo e sumario.

## Self-Check: PASSED
