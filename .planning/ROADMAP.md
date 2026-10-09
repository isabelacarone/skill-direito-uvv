# Roadmap: Skill ABNT UVV Direito

## Overview

A skill nasce em fatias que já funcionam sozinhas. Primeiro entra o modo Revisar, que exige a base de conhecimento do manual e as regras do curso. Depois o modo Formatar, com referências de Direito e elementos pré-textuais. Em seguida o modo Checar documento, com o script que lê um .docx. Por fim, os casos de teste do briefing validam as três fatias juntas.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Revisar trechos** - Skill instalada e revisando citações, estilo e fundamentação com origem da regra (completed 2026-10-09)
- [ ] **Phase 2: Formatar elementos** - Geração de citações, referências (inclusive legislação e jurisprudência), legendas, capa, folha de rosto e sumário
- [ ] **Phase 3: Checar documento** - Script que relata a formatação gráfica de um .docx
- [ ] **Phase 4: Validação** - Os 8 casos de teste do briefing rodam e passam

## Phase Details

### Phase 1: Revisar trechos

**Goal**: A skill `abnt-uvv-direito` está instalada em `.claude/skills/` e devolve parecer e tabela de inconformidades para um trecho colado
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: BASE-01, BASE-02, BASE-03, BASE-04, REV-01, REV-02, REV-03, REV-04, QA-02
**Success Criteria** (what must be TRUE):

  1. Pedir "revise este trecho do meu TCC" aciona a skill e ela devolve parecer (Conforme / Ajustes necessários / Crítico) com diagnóstico curto
  2. Cada inconformidade na tabela traz trecho, origem da regra (item e página do manual, "Regra do curso" ou "NBR geral"), problema e correção reescrita
  3. Uma citação direta longa mal formatada, um *apud* invertido e uma afirmação sem fonte são todos apontados, esta última com `[Inserir autor, ano, p.]`
  4. Um trecho sem seção informada leva a skill a perguntar a seção, e uma regra fora dos documentos gera "não consta no manual" sem página inventada

**Plans:** 5/5 plans complete

Plans:
**Wave 1**

- [x] 01-01-PLAN.md — Ferramentas: mapa item → página impressa do manual, verificador de references/ e extrator dos .docx

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02-PLAN.md — references/formatacao-grafica.md e pre-textuais.md (manual 2.1, 2.2, cap. 3)
- [x] 01-03-PLAN.md — references/citacoes.md e tabelas-ilustracoes.md (manual caps. 4 e 5, 2.3.2)
- [x] 01-04-PLAN.md — references/referencias-direito.md e regras-curso-direito.md (cap. 6, Projeto, Estudo Dirigido)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-05-PLAN.md — SKILL.md do modo Revisar, verificador da skill, 6 casos e aprovação da autora

### Phase 2: Formatar elementos

**Goal**: A skill gera no padrão UVV os elementos que a autora pede, sem preencher dados que faltam
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: FMT-01, FMT-02, FMT-03, FMT-04, FMT-05, FMT-06
**Success Criteria** (what must be TRUE):

  1. Dado um autor, ano e página, a skill devolve citação direta curta, longa, indireta e com *apud* no padrão UVV
  2. Uma lista de referências de livro, artigo, capítulo, lei e acórdão sai em ordem alfabética, alinhada à esquerda, com 12 pt entre referências e links sem `< >`
  3. Capa, folha de rosto e sumário saem no modelo certo para Projeto de Pesquisa e para TCC final
  4. Quando falta ano, editora, página ou data de acesso, a skill pede o dado em vez de inventar

**Plans**: TBD

### Phase 3: Checar documento

**Goal**: A autora aponta um .docx e recebe um relatório objetivo da formatação gráfica
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: DOC-01, DOC-02, DOC-03
**Success Criteria** (what must be TRUE):

  1. O script lê um .docx e relata fonte, tamanho, margens, entrelinhas e alinhamento do corpo do texto
  2. O relatório aponta citações longas sem recuo de 4 cm ou fora de Arial 10, numeração de página e seção primária que não começa em página nova
  3. Cada item sai com ✔ ou ✘, e o que o script não alcança aparece como "verificar manualmente"

**Plans**: TBD

### Phase 4: Validação

**Goal**: Os casos de teste do briefing comprovam que as três fatias funcionam juntas
**Mode:** mvp
**Depends on**: Phase 2, Phase 3
**Requirements**: QA-01
**Success Criteria** (what must be TRUE):

  1. Os 8 casos da seção 9 do briefing estão registrados no repositório com a entrada e a saída esperada
  2. Cada caso foi executado contra a skill e passa; falhas viram correção antes de dar a skill por pronta

**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Revisar trechos | 5/5 | Complete   | 2026-10-09 |
| 2. Formatar elementos | 0/TBD | Not started | - |
| 3. Checar documento | 0/TBD | Not started | - |
| 4. Validação | 0/TBD | Not started | - |
