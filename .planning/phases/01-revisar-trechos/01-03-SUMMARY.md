---
phase: 01-revisar-trechos
plan: 03
subsystem: references
tags: [abnt, manual-uvv, citacoes, tabelas, references, markdown]

requires:
  - phase: 01-01
    provides: "manual_mapa.json, checar_references.py, manual_paginas.py"
provides:
  - "references/citacoes.md: 42 regras CIT (manual cap. 4, p. 36-52, mais limite de 10 linhas do curso)"
  - "references/tabelas-ilustracoes.md: 20 regras TAB (cap. 5, p. 53-55, e 2.3.2, p. 29-30)"
affects: [01-04, 01-05]

key-files:
  created:
    - .claude/skills/abnt-uvv-direito/references/citacoes.md
    - .claude/skills/abnt-uvv-direito/references/tabelas-ilustracoes.md

key-decisions:
  - "Fonte obrigatoria de toda citacao ancorada no texto do manual (item 4, p. 36), nao em NBR"
  - "Sub-itens 4.4.6.1 a 4.4.6.4 agrupados em CIT-24 com origem 4.4.6, p. 43, por nao estarem no mapa"
  - "Apud invertido gravado como regra derivada da ordem do texto (4.3, p. 39-40), com exemplo do briefing"

requirements-completed: [BASE-02, REV-03]

duration: 25min
completed: 2026-10-09
---

# Phase 1 Plan 03: citacoes e tabelas-ilustracoes Summary

**62 regras condensadas (42 CIT + 20 TAB) com item e pagina impressa do manual, validadas por checar_references.py (0 erros), cobrindo apud, citacao longa, supressao, notas, tabelas, ilustracoes, apendices e anexos.**

## Paginas conferidas
Texto extraido (pdftotext) de todas as paginas impressas 36-52, 29-31 e 53-55 e lido integralmente.
Renderizadas e vistas como imagem: 37, 40, 51, 52 (citacoes); 30, 54, 55 (tabelas/apendices).
As demais (38-39, 41-50, 29, 31, 53) foram conferidas so pelo texto extraido, nao pela imagem.

## Task Commits
1. Task 1 citacoes.md: dd04909
2. Task 2 tabelas-ilustracoes.md: 2a53e42

## Deviations from Plan

### Divergencias registradas
- **Item 4.1.9:** nao citado (so existe no sumario, regra do verificador).
- **Afirmacao sem fonte:** o manual sustenta a regra (p. 36, "a fonte ... deve, obrigatoriamente, ser citada"); origem Manual 4, p. 36, sem recorrer a NBR 10520.
- **Apud (CIT-16):** os exemplos da p. 40 variam a pontuacao antes de "apud"; gravado o texto da regra, com Nota.
- **Item 4.4.6.x:** sub-itens ausentes do mapa; unificados em CIT-24 sob 4.4.6, p. 43 (o texto dos sub-itens esta nas p. 43-45).
- **Apud invertido (CIT-17):** o manual nao fala em "invertido"; regra derivada da ordem do texto (4.3), exemplo vindo do briefing.
- **Tabelas:** o manual traz as normas IBGE e "continua/continuacao/conclusao" (5.1, p. 53), entao nao houve necessidade de origem "NBR geral". O exemplo de tabela da p. 54 mostra "Tabela 2" sob a legenda "Figura 15"; nao usado como regra.
- **Numeracao de notas:** 4.5.1 recomenda reiniciar por capitulo e 4.5.2 exige numeracao unica por capitulo; ambos proibem reinicio por pagina (CIT-40, CIT-43).
- **Limite de 10 linhas (CIT-07):** origem Regra do curso (Projeto de Pesquisa, Orientacoes Gerais); regra completa em 01-04.

Nenhum auto-fix de codigo.

## Known Stubs
None.

## Self-Check: PASSED
- Dois arquivos existem; commits dd04909 e 2a53e42 presentes; verificador: 118 regras no diretorio, 0 erros; testes unittest OK.
