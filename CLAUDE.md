<!-- GSD:project-start source:PROJECT.md -->
## Project

**Skill ABNT UVV Direito**

Uma skill do Claude Code, `abnt-uvv-direito`, que audita e formata o Projeto de Pesquisa (Monografia I) e o TCC do curso de Direito da UVV segundo o Manual de Normas ABNT da UVV (2024) e as regras do curso. Uso pessoal da autora (Victória), instalada neste repositório em `.claude/skills/`. O briefing completo está em `PROMPT-SKILL-ABNT-UVV.md`.

**Core Value:** Dar à autora um parecer e uma formatação confiáveis, com cada regra apontando a origem (item e página do manual, regra do curso ou NBR), sem nunca inventar fonte, dado de obra ou página.

### Constraints

- **Fontes**: apenas os três documentos em `docs/` como base normativa — regra ausente deve ser declarada como "não consta no manual"
- **Instalação**: skill em `.claude/skills/abnt-uvv-direito/` deste repositório — decisão da autora
- **Estrutura**: SKILL.md curto + `references/` carregados sob demanda — evita gastar contexto
- **Script**: Python com python-docx — necessário para ler formatação de .docx
- **Conta**: código e materiais ficam na conta pessoal; nada da Elo
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
