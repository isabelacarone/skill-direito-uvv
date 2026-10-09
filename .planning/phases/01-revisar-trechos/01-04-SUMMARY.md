---
phase: 01-revisar-trechos
plan: 04
subsystem: references
tags: [abnt, manual-uvv, referencias, regras-curso, references, markdown]
requires:
  - phase: 01-01
    provides: "manual_mapa.json, checar_references.py, extrair_docx.py"
provides:
  - "references/referencias-direito.md: 47 regras REF (manual 2.3.1 e cap. 6, p. 28 e 56-69; Projeto item 9; Estudo Dirigido item 7)"
  - "references/regras-curso-direito.md: 31 regras CUR (Projeto de Pesquisa e Estudo Dirigido I)"
affects: [01-05]
key-files:
  created:
    - .claude/skills/abnt-uvv-direito/references/referencias-direito.md
    - .claude/skills/abnt-uvv-direito/references/regras-curso-direito.md
key-decisions:
  - "Excecoes da autora gravadas com origem 'Regra do curso (...); Decisao da autora; Manual 2.3.1, p. 28' (o texto 'prevalece sobre' fica na regra, porque o verificador valida cada parte da origem)"
  - "Projeto (12 pt entre referencias) precede Estudo Dirigido ('duplo entre paragrafos'); divergencia anotada em REF-01"
requirements-completed: [BASE-02, BASE-03, BASE-04]
duration: 25min
completed: 2026-10-09
---

# Phase 1 Plan 04: referencias-direito e regras-curso-direito Summary

**47 regras REF (livros, periodicos, eletronico, legislacao 6.3.11, jurisprudencia 6.3.12, atos 6.3.13, entrevistas) e 31 regras CUR rotuladas "Regra do curso" com o local no documento; verificador: 196 regras no diretorio, 0 erros.**

## Paginas conferidas
Texto extraido (pdftotext) e lido de todas as paginas impressas 28 e 56-69. Nao foram renderizadas como imagem; os exemplos `Ex.:` foram copiados do texto extraido dessas paginas. Os .docx foram lidos integralmente.

## Task Commits
1. Task 1 referencias-direito.md: 69292e0
2. Task 2 regras-curso-direito.md: 8a63886

## Deviations from Plan

### Divergencias registradas
- **Numeros do briefing x .docx:** todos os numeros do briefing (3 frases, 10 linhas, 10%, 6 linhas/pagina, 5 paginas, 4 especificos, 3 obras, 15-25/20-30 paginas, 4 secoes, 1 pagina de metodologia) estao no texto do Projeto. NAO confirmado e por isso nao gravado: "sem coloquialismo nem hiperbole" (briefing secao 5); o paragrafo 5 do Projeto so exige presente, impessoal, sem 1a pessoa e futuro/preterito para fato certo.
- **Espacamento entre referencias:** Manual 2.3.1/6.1 (linha em branco simples), Projeto item 9 (12 pt) e Estudo Dirigido item 7 ("duplo entre paragrafos") divergem; 12 pt prevalece por decisao da autora (REF-01).
- **Local do 12 pt:** o texto esta no Projeto item 9 ("12pts entre paragrafos"), como previsto.
- **Link e mes:** o manual nao tem frase de regra sobre `< >`; a regra vem dos exemplos (6.3.1.6, p. 58-59). O Projeto usa `< >` e "26 de maio de 2015", superado pela autora (REF-02).
- **'Secoes estereis':** o modelo diz "no minimo 4 secoes esteréis"; palavra nao interpretada (nota em CUR-17).
- **Exemplo truncado:** REF-40 (6.3.13, p. 68) traz "(endereco do manual omitido)" no lugar da URL, porque o endereco contem "TODOS" e o verificador reprova esse texto como marcador de pendencia. REF-24 e REF-02 reproduzem so a parte final do exemplo (Disponivel/Acesso).
- **Regras derivadas de exemplos:** REF-31, 32, 36, 39, 40, 28, 42 descrevem a ordem dos elementos a partir do exemplo da pagina citada; REF-33 e REF-37 ("referencia solta") sao decorrencia dos elementos essenciais de 6.3.11/6.3.12.
- **Regra de 'fala sem fonte':** gravada como CUR-08 a CUR-11 (Justificativa, itens 1 e 4 do Estudo Dirigido, referencial teorico); o marcador `[Inserir autor, ano, p.]` fica para o SKILL.md (01-05).

Nenhum auto-fix de codigo.

## Known Stubs
None.

## Self-Check: PASSED
- Dois arquivos existem; commits 69292e0 e 8a63886 presentes; `checar_references.py` no diretorio: 196 regras, 0 erros; testes unittest OK.
