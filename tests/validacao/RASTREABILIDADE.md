# Rastreabilidade dos 8 casos do briefing

Os 8 casos da seção 9 do briefing já estão cobertos pelos casos fixos das Fases 1 a 3; nenhum foi duplicado. Cada linha aponta o arquivo com a entrada e a saída esperada.

| Caso | Briefing (§9) | Arquivo | Modo | O que o caso exige |
|---|---|---|---|---|
| 1 | Citação direta de 5 linhas no corpo, com aspas e sem recuo | `tests/revisar/caso-01-citacao-longa.md` | Revisar | Parecer Ajustes necessários; recuo de 4 cm, Arial 10, sem aspas (Manual 4.1.3, p. 37); chamada (Streck, 2017, p. 25) |
| 2 | `Segundo Streck (2017, p. 25 apud Freire, 1994)` | `tests/revisar/caso-02-apud-invertido.md` | Revisar | Parecer Crítico; apud invertido (Manual 4.3, p. 39–40); correção Segundo Freire (1994 apud Streck, 2017, p. 25) |
| 3 | Lei e acórdão do STF soltos | `tests/formatar/caso-05-lei-acordao-soltos.md` | Formatar | Lei no padrão 6.3.11 (p. 66); acórdão só após perguntar relator e data de julgamento (6.3.12), sem inventar dados |
| 4 | Parágrafo com afirmação estatística sem chamada | `tests/revisar/caso-03-afirmacao-sem-fonte.md` | Revisar | Parecer Crítico; marcador [Inserir autor, ano, p.]; pede a fonte do dado |
| 5 | Parágrafo em 1ª pessoa com duas frases | `tests/revisar/caso-06-primeira-pessoa.md` | Revisar | Aponta a 1ª pessoa e a regra das 3 frases (regra do curso), correção impessoal |
| 6 | Trecho sem indicar a seção | `tests/revisar/caso-04-sem-secao.md` | Revisar | Só a pergunta pela seção, sem parecer nem tabela |
| 7 | .docx com margens de 2,5 cm e Times New Roman | `tests/checar/caso-01-margem-fonte.md` | Checar documento | ✘ em margens (GRA-09) e fonte (GRA-03), demais ✔ |
| 8 | Pedido de regra que o manual não cobre | `tests/revisar/caso-05-fora-do-manual.md` | Revisar | "Não consta no manual", sem página nem exemplo inventado |

## Outros casos fixos (contexto, fora do briefing)

20 casos fixos no total, 8 mapeados acima. Os outros 12:

- tests/formatar: caso-01 a caso-04 e caso-06 a caso-10 (9 casos)
- tests/checar: caso-02, caso-03 e caso-04 (3 casos)
