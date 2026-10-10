---
quick: 261009-vi8
status: complete
commit: 3786705
---

# Quick 261009-vi8: ignorar docs/ e o briefing

- `.gitignore` agora ignora `docs/` e `PROMPT-SKILL-ABNT-UVV.md` (e mantém `__pycache__/`, sem a linha em branco extra).
- `git status --short` não lista mais os dois; `git check-ignore -v` confirma as regras nas linhas 4 e 5.
- `python tools/validar_tudo.py` continua `validacao ok`: as ferramentas leem docs/ localmente, o que o ignore não afeta.
- Nada de docs/, do briefing, do 01-UAT.md ou de .planning/config.json foi commitado.
- Execução inline pelo orquestrador (sem planejador/executor), por ser edição de 3 linhas.
