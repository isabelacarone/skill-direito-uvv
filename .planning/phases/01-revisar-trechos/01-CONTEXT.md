# Phase 1: Revisar trechos - Context

**Gathered:** 2026-10-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Instalar a skill `abnt-uvv-direito` em `.claude/skills/` e fazer o modo Revisar devolver parecer (Conforme / Ajustes necessários / Crítico) e tabela de inconformidades com origem da regra para um trecho colado. Inclui a base de conhecimento em `references/` e a precedência de fontes. Formatar (Fase 2) e o script de .docx (Fase 3) ficam fora.

</domain>

<decisions>
## Implementation Decisions

### Construção de references/
- **D-01:** Cada regra é escrita de forma condensada (1–2 linhas) com item e página, mais um exemplo curto do manual quando ajudar. Não copiar o texto do manual quase literal.
- **D-02:** Citar a **página impressa** do manual, como o briefing faz (ex.: "Manual 4.1.3, p. 37"). Extrair o texto do PDF e conferir cada regra, uma a uma, contra a página renderizada antes de gravar. Não gravar página sem conferir.
- **D-03:** `references/` segue os 6 arquivos do briefing: `formatacao-grafica.md`, `pre-textuais.md`, `citacoes.md`, `tabelas-ilustracoes.md`, `referencias-direito.md`, `regras-curso-direito.md`. O SKILL.md indica qual abrir por tipo de pedido.
- **D-04:** Conflito entre Manual, Projeto e Estudo Dirigido: aplicar a precedência (Manual → Projeto → Estudo Dirigido → NBR) e registrar a origem na coluna "Origem da regra". Mencionar a divergência só quando ela mudar a correção.

### Claude's Discretion
- Escopo da base na Fase 1: escrever os 6 arquivos agora ou só os que o Revisar usa (BASE-02 lista todos os capítulos).
- Régua do parecer: o que separa Conforme / Ajustes necessários / Crítico, e quanto o tamanho do trecho encurta a saída.
- Entradas ainda não cobertas: resposta a caminho de .docx (script só na Fase 3), pedido de formatar (Fase 2) e trecho sem tipo de documento (Projeto vs TCC). Guiar-se pelo briefing, seções 3 e 6.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Briefing e requisitos
- `PROMPT-SKILL-ABNT-UVV.md` — briefing completo: fontes e precedência (§2), entrada (§3), regras normativas (§4), regras do curso (§5), formato de saída (§6), guardrails (§7), estrutura de arquivos (§8), casos de teste (§9)
- `.planning/REQUIREMENTS.md` — BASE-01..04, REV-01..04, QA-02
- `.planning/ROADMAP.md` — objetivo e critérios de sucesso da Fase 1
- `.planning/PROJECT.md` — decisões-chave e restrições

### Fontes normativas
- `docs/MANUAL ABNT 2024 uvv.pdf` — fonte principal (72 p.); citar item e página impressa
- `docs/001 - Projeto de Pesquisa - Atualizado.docx` — regras do curso e padrão de referências de Direito (item 9). As p. 13–14 ainda não foram renderizadas para confirmar
- `docs/Direito - Estudo Dirigido I - 2026-2.docx` — exigências de fontes e lista de referências (item 7). A p. 3 ainda não foi renderizada para confirmar

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Nenhum: repositório sem código; `.claude/skills/` ainda não existe.

### Established Patterns
- SKILL.md curto + `references/` carregados sob demanda (restrição do projeto).

### Integration Points
- Skill instalada em `.claude/skills/abnt-uvv-direito/` deste repositório, com frontmatter `name` e `description` que dispara em pedidos de revisão de TCC e Projeto de Pesquisa.

</code_context>

<specifics>
## Specific Ideas

- O manual tem pequenas falhas internas (ex.: remete à "Figura 13" para a margem, que está na Figura 14). Em dúvida entre texto e exemplo, vale o texto da regra.
- Agentes GSD de pesquisa não estão instalados em `.claude-pessoal/agents`; se o plano pedir pesquisa, instalá-los antes.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 1-Revisar trechos*
*Context gathered: 2026-10-09*
