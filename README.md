# Skill ABNT UVV Direito

Skill do Claude Code (`abnt-uvv-direito`) que audita e formata o Projeto de Pesquisa (Monografia I) e o TCC do curso de Direito da UVV. A única base normativa são os três documentos de `docs/`; regra que eles não trazem é declarada como "não consta no manual".

## Onde está

`.claude/skills/abnt-uvv-direito/`, usada pela conta pessoal do Claude Code. Numa sessão nova, `/skills` deve listar `abnt-uvv-direito`.

## Os três modos

- **Revisar**: cole um trecho e diga a seção (ex.: "revise este trecho da introdução"). Sai um parecer com a origem de cada regra.
- **Formatar**: peça a citação, a referência ou o elemento pré-textual e informe os dados (ex.: "formate esta referência de livro: autor, título, editora, ano").
- **Checar documento**: aponte o caminho de um .docx (ex.: "cheque `C:\caminho\meu-trabalho.docx`"). Exige `python` e `pip install python-docx`.

## Como validar

```
python tools/validar_tudo.py          # verificadores automáticos
python tools/validar_tudo.py --final  # exige também os 8 casos do briefing como "passou"
```

Os casos fixos ficam em `tests/` (revisar, formatar, checar). O mapa dos 8 casos do briefing e o registro dos resultados ficam em `tests/validacao/` (`RASTREABILIDADE.md` e `RESULTADOS.md`).
