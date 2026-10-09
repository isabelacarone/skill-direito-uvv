# Skill ABNT UVV Direito

## What This Is

Uma skill do Claude Code, `abnt-uvv-direito`, que audita e formata o Projeto de Pesquisa (Monografia I) e o TCC do curso de Direito da UVV segundo o Manual de Normas ABNT da UVV (2024) e as regras do curso. Uso pessoal da autora (Victória), instalada neste repositório em `.claude/skills/`. O briefing completo está em `PROMPT-SKILL-ABNT-UVV.md`.

## Core Value

Dar à autora um parecer e uma formatação confiáveis, com cada regra apontando a origem (item e página do manual, regra do curso ou NBR), sem nunca inventar fonte, dado de obra ou página.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Modo **Revisar**: parecer (Conforme / Ajustes necessários / Crítico), tabela de inconformidades com origem da regra, checagem de fundamentação e próximos passos
- [ ] Modo **Formatar**: gerar citação, referência (inclusive legislação, jurisprudência e atos normativos), legenda de tabela/figura, capa, folha de rosto e sumário no padrão UVV
- [ ] Modo **Checar documento**: script `verificar_docx.py` (python-docx) que relata fonte, margens, entrelinhas, recuo de citação longa, numeração de página e hierarquia de títulos de um .docx
- [ ] Base de conhecimento em `references/` derivada do manual (caps. 2–6), do Projeto de Pesquisa e do Estudo Dirigido, com páginas citáveis
- [ ] Regras do curso de Direito aplicadas: parágrafo de 3 frases, citação longa até 10 linhas, máximo 10% de citação direta, tempo presente e impessoal, mínimos do Projeto
- [ ] Precedência de fontes implementada: Manual UVV → Projeto de Pesquisa → Estudo Dirigido → NBR geral, com exceção de 12 pt entre referências
- [ ] Padrão de links: `Disponível em: url. Acesso em: 26 jun. 2019.` sem `< >`, mês abreviado
- [ ] Guardrails: nunca inventar autor, ano, página, processo ou lei; pedir o dado que faltar; alterar forma, não mérito
- [ ] 8 casos de teste do briefing (seção 9) executados e aprovados

### Out of Scope

- Ficha catalográfica — a autora decidiu que não é necessária
- Distribuição para outros alunos — uso pessoal, sem generalização por enquanto
- Instalação global em `.claude-pessoal/skills/` — decisão: skill só neste repositório
- Conteúdo jurídico do trabalho — a skill corrige forma e fundamentação, não a tese

## Context

- Fontes em `docs/`: `MANUAL ABNT 2024 uvv.pdf` (72 p.), `001 - Projeto de Pesquisa - Atualizado.docx`, `Direito - Estudo Dirigido I - 2026-2.docx`
- As páginas 13–14 do Projeto de Pesquisa e a página 3 do Estudo Dirigido parecem tratar de referências (item 9 e item 7); não foram renderizadas para confirmar
- O manual tem pequenas inconsistências internas; vale o texto da regra, não o exemplo
- Link do repositório de normas da UVV: https://repositorio.uvv.br/handle/123456789/88
- Ambiente: Windows 11, conta pessoal do Claude (Pro); repositório novo, sem código

## Constraints

- **Fontes**: apenas os três documentos em `docs/` como base normativa — regra ausente deve ser declarada como "não consta no manual"
- **Instalação**: skill em `.claude/skills/abnt-uvv-direito/` deste repositório — decisão da autora
- **Estrutura**: SKILL.md curto + `references/` carregados sob demanda — evita gastar contexto
- **Script**: Python com python-docx — necessário para ler formatação de .docx
- **Conta**: código e materiais ficam na conta pessoal; nada da Elo

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Precedência Manual → Projeto → Estudo Dirigido → NBR | Confirmada pela autora | — Pending |
| 12 pt entre referências (Projeto), não linha em branco (manual) | Decisão da autora | — Pending |
| Links sem `< >`, mês abreviado | Padrão do manual / NBR 6023:2020 | — Pending |
| Ficha catalográfica fora do escopo | Não é necessária | — Pending |
| v1 com os três modos | Autora quer revisar, formatar e checar .docx | — Pending |
| Skill só neste repositório | Decisão da autora | — Pending |
| Uso pessoal | Pode assumir dados da autora, sem generalizar | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-10-09 after initialization*
