---
phase: 03-checar-documento
plan: 02
subsystem: skill
tags: [abnt, docx, python-docx, verificador, modo-checar, citacao, numeracao, titulos]
requires:
  - phase: 03-checar-documento
    provides: verificar_docx.py (verificar, formatar, origem, LIMIARES, partes_do_documento, nivel_titulo)
provides:
  - itens_citacao, itens_numeracao, itens_titulos em verificar_docx.py
  - campos_pagina, tem_quebra_antes, tipo_secao_do_paragrafo
  - Fixture ficticia tests/checar/caso-02-citacao-titulos.docx
affects: [03-03]
tech-stack:
  added: []
  patterns: ["tipo da secao vem do w:sectPr que a ENCERRA, nao do anterior", "o que depende da paginacao do Word vai so para Verificar manualmente"]
key-files:
  created:
    - tests/checar/caso-02-citacao-titulos.docx
  modified:
    - .claude/skills/abnt-uvv-direito/scripts/verificar_docx.py
    - tests/checar/gerar_fixtures.py
    - tools/tests/test_verificar_docx.py
key-decisions:
  - "Campo PAGE lido por regex \\bPAGE\\b em fldSimple e instrText; nunca avaliado"
  - "titulo_numeracao vai para Verificar manualmente se qualquer titulo do corpo nao tem numero no texto"
requirements-completed: [DOC-02, DOC-03]
duration: 35min
completed: 2026-10-09
---

# Phase 3 Plan 2: Citacao longa, numeracao de pagina e titulos Summary

**`verificar_docx.py` passa a relatar recuo, fonte, entrelinhas e aspas da citacao longa (CIT-06), posicao, alinhamento, fonte e formato da numeracao (GRA-12/13) e quebra de pagina, grafia por nivel e numeracao consecutiva dos titulos (GRA-15/16/18); inicio da numeracao, 10 linhas e citacao sem recuo ficam so em "Verificar manualmente".**

## Tasks

1. Task 1: `6cd8e01` fixture caso-02 e testes (RED: 17 testes novos falhando, os de 03-01 passando).
2. Task 2: `db48f47` itens de citacao, numeracao e titulos (GREEN: 50 testes OK).

## Verificacao

`python -m unittest discover -s tools/tests` OK (50 testes); `checar_references.py` 243 regras, 0 erros. CLI: caso-01 com 2 cross (`| ✘ |` = 2: margens e fonte); caso-02 sai 1 com CIT-06, GRA-12, GRA-13, GRA-16, GRA-18 e GRA-15; caso-03 sai 0 (17 check, 0 cross, 3 verificar manualmente com GRA-11 e CIT-07). grep de `.save(`/subprocess/rede = 0; grep de nomes reais na fixture = 0. caso-01 e caso-03 regerados tem o mesmo conteudo de antes (todas as partes do zip iguais) e foram restaurados com `git checkout`; so caso-02 entrou no commit.

## Limitação

Citação longa com recuo < 1,5 cm e em Arial 12 não é candidata (P-21): não recebe ✔ nem ✘ e só aparece, quando tem aspas e mais de 225 caracteres entre elas, na estimativa de `citacao_sem_recuo` em "Verificar manualmente". Os itens `citacao_recuo`, `citacao_fonte`, `citacao_entrelinhas` e `citacao_aspas` só alcançam candidatos (recuo >= 1,5 cm, fonte <= 11 pt ou estilo de citação).

## Deviations from Plan

**1. [Rule 1 - Bug] HeaderPart nao tem `styles`**
- **Found during:** Task 2 (teste do campo precedido de tabulacao)
- **Issue:** `_doc_defaults` usava `par.part.styles`; em paragrafos de cabecalho/rodape levanta AttributeError quando nada na cadeia define o alinhamento.
- **Fix:** cai para `par.part._document_part.styles` quando a parte nao tem `styles`.
- **Commit:** db48f47

**2. [Rule 1 - Plano x realidade] Documentos de teste sem candidata a citacao**
- **Issue:** o Normal do template do python-docx e 11 pt; pela heuristica de P-21 (fonte <= 11 pt) todo o corpo viraria candidato. O teste `citacao_longa` montou o documento sem ajustar o tamanho.
- **Fix:** `doc_simples` do teste fixa o Normal em 12 pt. Nenhuma mudanca de regra.
- **Commit:** db48f47

**3. [Rule 1 - Plano x realidade] Teste de 03-01 com `Resumo:` fixo**
- **Issue:** `test_caso03` exigia `Resumo: 5 ✔, 0 ✘, 0 verificar manualmente`, que deixa de valer com os itens novos e os 3 itens manuais.
- **Fix:** regex `Resumo: \d+ ✔, 0 ✘, \d+ verificar manualmente` (commit 6cd8e01); o relatorio atual do caso-03 e `17 ✔, 0 ✘, 3 verificar manualmente`.

## Known Stubs

None.

## Threat Flags

None. Campos lidos so por regex (T-03-06); itens dependentes de paginacao so em "Verificar manualmente" (T-03-07); fixture ficticia (T-03-09).

## Self-Check: PASSED
