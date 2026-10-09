# Requirements: Skill ABNT UVV Direito

**Defined:** 2026-10-09
**Core Value:** Parecer e formatação confiáveis, com cada regra apontando a origem (item e página do manual, regra do curso ou NBR), sem inventar fonte, dado de obra ou página.

## v1 Requirements

### Base de conhecimento

- [x] **BASE-01**: A skill existe em `.claude/skills/abnt-uvv-direito/` com SKILL.md curto e frontmatter (name, description) que dispara em pedidos de revisão/formatação de TCC e Projeto de Pesquisa de Direito da UVV
- [x] **BASE-02**: `references/` contém as regras do manual (formatação gráfica, pré-textuais, citações, tabelas e ilustrações, referências) com item e página citáveis
- [x] **BASE-03**: `references/regras-curso-direito.md` contém as regras do Projeto de Pesquisa (parágrafo de 3 frases, citação longa até 10 linhas, máximo 10% de citação direta, tempo presente impessoal, mínimos por seção)
- [x] **BASE-04**: A precedência Manual → Projeto → Estudo Dirigido → NBR está declarada, com a exceção de 12 pt entre referências e o padrão de link sem `< >` e mês abreviado

### Revisar

- [x] **REV-01**: Dado um trecho e a seção do trabalho, a skill devolve parecer (Conforme / Ajustes necessários / Crítico) com 2 a 4 frases de diagnóstico
- [x] **REV-02**: A skill devolve tabela de inconformidades em que cada linha traz trecho original, origem da regra (item e página, "Regra do curso" ou "NBR geral"), problema e correção já reescrita
- [x] **REV-03**: A skill aponta afirmação sem fonte com `[Inserir autor, ano, p.]`, *apud* invertido, página ausente em citação direta e supressão mal marcada
- [x] **REV-04**: Se o trecho vier sem a seção do trabalho, a skill pergunta a seção antes de avaliar

### Formatar

- [x] **FMT-01**: A skill gera citação direta curta, direta longa (recuo 4 cm, Arial 10, sem aspas), indireta e *apud* no padrão UVV
- [x] **FMT-02**: A skill formata referências de livro, capítulo, artigo, trabalho acadêmico, site, evento e entrevista; 12 pt entre referências, alinhadas à esquerda
- [ ] **FMT-03**: A skill formata referências de legislação, jurisprudência e atos administrativos normativos (manual 6.3.11 a 6.3.13)
- [ ] **FMT-04**: A skill gera legenda de tabela, figura e quadro com título acima e `Fonte:` abaixo
- [ ] **FMT-05**: A skill gera capa, folha de rosto e sumário nos dois modelos (Projeto/Monografia I e TCC final)
- [x] **FMT-06**: Quando faltar dado (ano, editora, página, data de acesso), a skill pede o dado e nunca preenche por conta própria

### Checar documento

- [ ] **DOC-01**: `scripts/verificar_docx.py` relata fonte e tamanho, margens, entrelinhas e alinhamento de um .docx
- [ ] **DOC-02**: O script relata recuo e fonte de citações longas, numeração de página e hierarquia de títulos (seção primária em página nova)
- [ ] **DOC-03**: O relatório marca ✔/✘ por item e lista o que precisa de verificação manual

### Qualidade

- [ ] **QA-01**: Os 8 casos de teste da seção 9 do briefing passam e ficam registrados no repositório
- [x] **QA-02**: Regra fora dos três documentos gera a resposta "não consta no manual", sem página inventada

## v2 Requirements

- **V2-01**: Verificar o limite de 10% de citação direta no documento inteiro
- **V2-02**: Gerar sumário a partir da estrutura do .docx
- **V2-03**: Incluir `modelo-projeto-pesquisa.docx` em `assets/`

## Out of Scope

| Feature | Reason |
|---------|--------|
| Ficha catalográfica | Decisão da autora: não é necessária |
| Distribuição para outros alunos | Uso pessoal por enquanto |
| Instalação global em `.claude-pessoal/skills/` | Skill fica só neste repositório |
| Revisão do mérito jurídico | A skill corrige forma e fundamentação, não a tese |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 1 | Complete |
| BASE-02 | Phase 1 | Complete |
| BASE-03 | Phase 1 | Complete |
| BASE-04 | Phase 1 | Complete |
| REV-01 | Phase 1 | Complete |
| REV-02 | Phase 1 | Complete |
| REV-03 | Phase 1 | Complete |
| REV-04 | Phase 1 | Complete |
| FMT-01 | Phase 2 | Complete |
| FMT-02 | Phase 2 | Complete |
| FMT-03 | Phase 2 | Pending |
| FMT-04 | Phase 2 | Pending |
| FMT-05 | Phase 2 | Pending |
| FMT-06 | Phase 2 | Complete |
| DOC-01 | Phase 3 | Pending |
| DOC-02 | Phase 3 | Pending |
| DOC-03 | Phase 3 | Pending |
| QA-01 | Phase 4 | Pending |
| QA-02 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-10-09*
*Last updated: 2026-10-09 after initial definition*
