# Skill ABNT UVV Direito

Uma skill do Claude (`abnt-uvv-direito`) que **revisa, formata e confere** o Projeto de Pesquisa (Monografia I) e o TCC do curso de Direito da UVV, segundo o *Manual de Normas ABNT da UVV (2024)* e as regras do curso.

Cada correção aponta de onde veio a regra: item e página impressa do manual, regra do curso ou NBR. O que o manual não cobre é respondido como **"não consta no manual UVV"**, sem inventar página. A skill nunca inventa autor, ano, página, editora, número de processo ou acórdão: quando falta dado, ela pede.

> Projeto pessoal e não oficial. Não é da UVV nem foi validado por ela. Confirme dúvidas com a Biblioteca Central e com o seu orientador; o manual vigente fica em <https://repositorio.uvv.br/handle/123456789/88>.

## O que ela faz

| Modo | Você pede | Você recebe |
|---|---|---|
| **Revisar** | Cola um trecho e diz a seção (Introdução, Justificativa, Considerações Finais…) | Parecer (`Conforme`, `Ajustes necessários` ou `Crítico`), tabela de inconformidades com a origem de cada regra e a correção já reescrita |
| **Formatar** | Pede uma citação, referência, legenda, capa, folha de rosto ou sumário e informa os dados | O elemento pronto para colar, com a regra aplicada. Se faltar dado, a skill pergunta |
| **Checar documento** | Aponta um arquivo `.docx` | Relatório com ✔ ou ✘ por item (fonte, tamanho, margens, entrelinhas, alinhamento, citação longa, numeração de página, títulos) e uma lista do que precisa conferir à mão |

Ela altera a **forma**, nunca o mérito: a tese e o argumento são seus.

## Como instalar

### No Claude Code (mais simples)

```bash
git clone https://github.com/isabelacarone/skill-direito-uvv.git
cd skill-direito-uvv
claude
```

Dentro da pasta, a skill é carregada de `.claude/skills/abnt-uvv-direito/`. Rode `/skills` para confirmar que `abnt-uvv-direito` aparece.

Para usar em outro projeto, copie a pasta `.claude/skills/abnt-uvv-direito/` para `.claude/skills/` desse projeto (ou para `~/.claude/skills/`, para todos os projetos).

### No Claude Desktop ou no claude.ai

Baixar o ZIP do repositório **não** serve: a skill fica dentro de `.claude/skills/`. Crie um ZIP só com a pasta `abnt-uvv-direito/` (o `SKILL.md` precisa estar dentro dela) e carregue nas configurações de skills do app. O nome do menu varia com a versão, e skills dependem do plano e da execução de código estarem ativados.

Esse caminho **não foi testado**: a skill foi validada só no Claude Code.

## Como usar

Escreva em linguagem natural. Exemplos:

- **Revisar:** `revise este trecho da Justificativa:` e cole o texto. Sem dizer a seção, a skill pergunta a seção e se o documento é Projeto ou TCC final antes de avaliar.
- **Formatar:** `formate esta referência de livro: autor, título, edição, local, editora, ano.` ou `gere a citação direta longa de Fulano (2017, p. 25).` Pode pedir também lei, acórdão, súmula, legenda de tabela, capa, folha de rosto e sumário (Projeto/Monografia I ou TCC final).
- **Checar documento:** `cheque a formatação de C:\caminho\meu-trabalho.docx`. Precisa de Python e do pacote `python-docx` (`pip install python-docx`). Sem isso, cole o trecho e peça a revisão.

Texto colado não mostra fonte, margem nem espaçamento. Para isso, use o modo Checar documento.

### Limites que você deve conhecer

- A checagem do `.docx` não renderiza o documento (sem LibreOffice): numeração de página por seção, quebras reais de página e contagem de linhas saem em "verificar manualmente".
- Uma citação longa com recuo menor que 1,5 cm e em Arial 12 não é detectada como candidata; aparece só como estimativa.
- A ficha catalográfica está fora do escopo.
- Quando o Manual, o Projeto de Pesquisa e o Estudo Dirigido divergem, vale a ordem **Manual → Projeto → Estudo Dirigido → NBR**, com duas exceções decididas pela autora: 12 pt entre referências (Projeto) e links sem `< >`, com mês abreviado (Manual).

## Como o repositório está organizado

```text
.claude/skills/abnt-uvv-direito/   a skill
  SKILL.md                         papel, modos, fluxo, formato de saída
  references/                      regras condensadas, com item e página (6 arquivos)
  scripts/verificar_docx.py        modo Checar documento
docs/                              material-fonte: manual UVV 2024 (PDF) e os dois .docx do curso
tools/                             verificadores e ferramentas de apoio (mapa de páginas, checadores)
tests/                             casos fixos de revisar, formatar e checar, e a validação dos 8 casos
.planning/                         planejamento e histórico do desenvolvimento (GSD)
```

## Como validar

```bash
python tools/validar_tudo.py          # verificadores automáticos
python tools/validar_tudo.py --final  # exige também os 8 casos do briefing como "passou"
python tools/manual_paginas.py texto 37   # texto da página impressa 37 do manual
```

Os 8 casos do briefing e o registro dos resultados estão em `tests/validacao/` (`RASTREABILIDADE.md` e `RESULTADOS.md`). A rodada registrada foi feita por Claude, a pedido da autora, e não numa sessão dela; isso consta no próprio arquivo.

## Materiais da UVV em `docs/`

`docs/` guarda o Manual de Normas ABNT da UVV (2024) e dois documentos do curso de Direito, usados como única base normativa da skill. São materiais institucionais da UVV: os direitos pertencem à UVV e aos autores, e os dados pessoais nos .docx foram trocados por marcadores (`NOME DO AUTOR`, `Autor`). A skill funciona sem `docs/`, porque as regras já estão condensadas em `references/`; a pasta serve para conferir páginas e rodar as ferramentas.
