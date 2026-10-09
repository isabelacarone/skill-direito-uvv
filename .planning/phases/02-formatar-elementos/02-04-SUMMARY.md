---
phase: 02-formatar-elementos
plan: 04
subsystem: skill
tags: [abnt, pre-textuais, capa, folha-de-rosto, sumario, modo-formatar]
requires:
  - phase: 02-formatar-elementos
    provides: fluxo do modo Formatar, checar_skill.py estendido a tests/formatar, casos 01-07 e 10
provides:
  - Modelos PRE-35 a PRE-41 (escolha por tipo de documento; capa, folha de rosto e sumario de Projeto e de TCC final)
  - tests/formatar caso-08 (Projeto) e caso-09 (TCC final com orientador faltante)
  - Aprovacao da autora dos 10 casos de tests/formatar
affects: []
tech-stack:
  added: []
  patterns: ["linha de modelo + bloco de layout com formatacao entre chaves; elemento com obrigatorio faltante fica retido"]
key-files:
  created:
    - tests/formatar/caso-08-pre-textuais-projeto.md
    - tests/formatar/caso-09-pre-textuais-tcc-final.md
  modified:
    - .claude/skills/abnt-uvv-direito/references/pre-textuais.md
    - tools/checar_references.py
key-decisions:
  - "Projeto: modelo do curso (docx); TCC final: Figuras 1, 2 e 11 transcritas das paginas renderizadas 9, 11 e 25 (P-14)"
  - "Texto da regra vence a figura ou o docx quando divergem; divergencia registrada em sub-linha Nota"
  - "Dados pessoais do modelo do curso nao entram em references/ nem nos casos (P-15)"
requirements-completed: [FMT-05, FMT-06]
duration: 40min
completed: 2026-10-09
---

# Phase 2 Plan 4: Pre-textuais e aprovacao Summary

**A skill gera capa, folha de rosto e sumario no modelo do curso (Projeto/Monografia I) ou no do manual (TCC final), pedindo orientador, titulo, local ou ano quando faltam; a autora rodou os 10 casos e aprovou.**

## Tasks

1. Task 1: `077d255` PRE-35 a PRE-41 em pre-textuais.md, a partir do docx do curso e das Figuras 1, 2 e 11 renderizadas; frase "nao ficam aqui" trocada.
2. Task 2: `27ee797` caso-08 (Projeto, tres blocos exatos, so 1 e 2.1 paginados) e caso-09 (TCC final: capa e sumario na primeira resposta, pergunta unica pelo orientador, folha de rosto depois).
3. Task 3: checkpoint humano. A autora respondeu "Aprovado" depois de rodar os 10 casos em sessao nova.

## Verificacao

`checar_references.py` 243 regras 0 erros; `checar_skill.py` skill ok; `--autoteste` ok; unittest OK; 10 casos em tests/formatar; greps de aceite conferidos (0 nomes reais).

## Deviations from Plan

**1. [Rule 3 - Blocking] Falso positivo de TODO no verificador**
- **Found during:** Task 1
- **Issue:** a regex de pendencia casava `TODO` dentro de "METODOLOGIA" (item 6 do sumario do Projeto).
- **Fix:** `TODO` passou a `\bTODO\b` em `tools/checar_references.py`; 0 erros, unittest OK.
- **Commit:** 077d255

**2. [Rule 1 - Plano x realidade] Titulo da capa do Projeto**
- **Issue:** o plano pedia titulo "TITULO DE TESTE" mais delimitacao no caso-08. No modelo do curso "PROJETO DE PESQUISA" e texto fixo e so ": SUBTITULO" e trocavel (CUR-13).
- **Fix:** linha `PROJETO DE PESQUISA: [DELIMITACAO DO TEMA]`; caso-08 sem titulo separado, delimitacao em caixa alta.
- **Commit:** 077d255, 27ee797

**3. Divergencias registradas em `Nota:` (vale o texto da regra)**
- Local e ano da capa sem negrito no docx, mas PRE-05 manda negrito.
- Nota da folha de rosto em Arial 11 no docx, PRE-10 manda Arial 10.
- Subtitulo em caixa alta na figura, PRE-04 so manda no titulo.
- "APENDICE" sem acento na Figura 11, usada a grafia correta.

**4. Lacunas das figuras preenchidas e anotadas**
- Marcadores "CURSO" e "Nome do Curso" trocados por Direito.
- Linha de coorientador inexistente nos modelos, segue o molde do orientador.
- Sumario do TCC inclui REFERENCIAS, anexos e apendices como na Figura 11; so pre-textuais ficam fora (PRE-27).

## Known Stubs

None.

## Self-Check: PASSED
