---
phase: quick-261009-up0
plan: 01
subsystem: skill-abnt-uvv-direito
tags: [skill, ambiguidades, qa-01]
requires: []
provides:
  - SKILL.md e references/ sem ambiguidade para os 8 casos do briefing
affects: [QA-01]
key-files:
  modified:
    - .claude/skills/abnt-uvv-direito/references/referencias-direito.md
    - .claude/skills/abnt-uvv-direito/SKILL.md
    - tests/formatar/caso-05-lei-acordao-soltos.md
decisions:
  - "REF-68 mantém a origem; o caso-05 formatar é que copia a origem de REF-68"
  - "Estimativa 225/650 vira seção compartilhada ## Estimativa de linhas"
metrics:
  completed: 2026-10-09
  tasks: 3
  files: 3
---

# Quick 261009-up0: ambiguidades da skill corrigidas

Régua do parecer, origem por linha, pergunta de seção, estimativa de linhas compartilhada, códigos de saída e ajustes de lei/acórdão passaram a ter uma única leitura em SKILL.md e references/; caso-05 (formatar) copia a origem de REF-68.

## Commits

- 42232fa: REF-63/67/68/69 e caso-05 formatar
- 1ac4720: SKILL.md (107 linhas)

## Mapeamento dos 8 casos

| Caso | Frase/linha que leva ao Esperado |
|---|---|
| revisar 01 (citação longa) | Régua: aspas mantidas ou só falta de recuo/fonte 10/entrelinha (CIT-06) = (b), Ajustes necessários; `## Estimativa de linhas` citada no passo 3; aviso de texto colado fecha o diagnóstico |
| revisar 02 (apud invertido) | Régua (a) apud invertido = Crítico; Formato de saída: página do original ausente é omitida (CIT-16); lembrete CIT-18 na coluna Correção ou no diagnóstico |
| revisar 03 (afirmação sem fonte) | Origem principal: CUR-08 na Justificativa, CIT-01 só complementar; `[Inserir autor, ano, p.]` na correção |
| revisar 04 (sem seção) | Passo 1 do Revisar: pergunta SEMPRE seção e tipo numa única mensagem |
| revisar 05 (fora do manual) | `## Regra que não está nas fontes`: abrir citacoes.md e referencias-direito.md antes de "não consta no manual UVV"; NBR sem página; Biblioteca Central |
| revisar 06 (1ª pessoa) | Régua: CUR-01..03 são (b)/(c) e levam a Ajustes necessários; linha de Introdução/Considerações Finais (CUR-23): conclusão própria sem chamada |
| formatar 05 (lei e acórdão) | REF-67/68/69/63: editor reduzido, jurisdição deduzida e marcadores em `Ajustes nos dados:`; origem da lei copiada de REF-68; acórdão retido com pergunta única (REF-69, passo 3 do Formatar) |
| checar 01 | Passo 5 do Checar: código 1 = há ✘ e relatório válido, entregue como veio |

## Deviations from Plan

**[Rule 1] REF-68 sem menção a `Ajustes nos dados:`** — a verificação exigia 4 linhas REF-63/67/68/69 com a expressão; REF-68 só remetia a REF-67. Acrescentei "(registrados em `Ajustes nos dados:`)" ao texto de REF-68. Incluído no commit 42232fa.

Nota: `validar_tudo.py` imprime "2 regras, 1 erros" (TAB-01, p. 50 fora do intervalo) em sua saída, mas termina com "validacao ok" (parte do autoteste negativo, comportamento anterior à tarefa).

## Verificação

`checar_skill.py` (skill ok), `--autoteste` (autoteste ok), `checar_references.py` (243 regras, 0 erros), `unittest` (OK), `validar_tudo.py` (validacao ok). QA-01 segue Pending; RESULTADOS.md, RASTREABILIDADE.md e REQUIREMENTS.md intocados; sem 4.1.9.

## Self-Check: PASSED
