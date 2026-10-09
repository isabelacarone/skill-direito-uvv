# Caso 09 - capa, folha de rosto e sumário do TCC final, com orientador faltante

## Entrada

Pedido: "Monte a capa, a folha de rosto e o sumário do meu TCC final." Dados fictícios:

- Autora: MARIA DE TESTE.
- Título: "TÍTULO DE TESTE: subtítulo de teste".
- Local e ano: Vila Velha, 2026.
- Orientador: não informado.
- Estrutura do trabalho: 1 INTRODUÇÃO (p. 8); 2 SEÇÃO DE TESTE (p. 10); 2.1 SUBSEÇÃO DE TESTE (p. 10); 2.1.1 Terciária de teste (p. 11); 3 CONSIDERAÇÕES FINAIS (p. 14); REFERÊNCIAS (p. 15).

## Esperado

Primeira resposta: a capa e o sumário já prontos, porque os obrigatórios deles estão completos, e uma única pergunta pedindo o orientador com titulação (e o coorientador, se houver). A folha de rosto não é entregue nesta rodada, e a resposta diz que ela depende do orientador (o obrigatório faltante retém só o elemento afetado).

Capa:

```
UNIVERSIDADE VILA VELHA
CURSO DE DIREITO
MARIA DE TESTE
TÍTULO DE TESTE: subtítulo de teste
VILA VELHA
2026
```

Sumário:

```
SUMÁRIO
1 INTRODUÇÃO ........................ 8
2 SEÇÃO DE TESTE .................... 10
2.1 SUBSEÇÃO DE TESTE ............... 10
2.1.1 Terciária de teste ............. 11
3 CONSIDERAÇÕES FINAIS .............. 14
REFERÊNCIAS ........................ 15
```

Depois da resposta "Prof. Dr. João de Teste", a folha de rosto no modelo do manual (Figura 2):

```
MARIA DE TESTE
TÍTULO DE TESTE: subtítulo de teste
Trabalho de Conclusão de Curso apresentado à Universidade Vila Velha como pré-requisito do Programa de Graduação em Direito.
Orientador: Prof. Dr. João de Teste.
VILA VELHA
2026
```

`Formatação no Word:` por linha, copiada das chaves dos modelos. Capa e folha de rosto: instituição, curso, nome da autora, título, local em negrito e centralizados, em caixa alta (o título em caixa alta e negrito, o subtítulo após os dois-pontos sem negrito e em minúsculas como foi escrito, PRE-04); ano em negrito e centralizado; "CURSO DE DIREITO" a 1,5 da linha acima. Nota e linha do orientador em Arial 10, justificadas, espaçamento simples, sem negrito, do centro à margem direita. Sumário: título em caixa alta, negrito, centralizado; "1 INTRODUÇÃO", "2 SEÇÃO DE TESTE", "3 CONSIDERAÇÕES FINAIS" e "REFERÊNCIAS" em caixa alta e negrito; "2.1 SUBSEÇÃO DE TESTE" em caixa alta sem negrito; "2.1.1 Terciária de teste" em negrito; páginas à direita com linha de pontos (GRA-18).

`Regra aplicada:` as origens das linhas de modelo, copiadas de `references/pre-textuais.md`: `Manual 2.1.1, p. 9`, `Manual 2.1.1, p. 8`, `Manual 2.1.2, p. 11`, `Manual 2.1.2, p. 10`, `Manual 2.1.9, p. 25`, `Manual 2.1.9, p. 24`, `Manual 3.4, p. 34`.

## Não pode

- Inventar orientador ou titulação, ou usar o nome de qualquer orientador real.
- Entregar a folha de rosto antes de ter o orientador.
- Usar o cabeçalho "MONOGRAFIA I", a sigla "UVV" ou "D8Ma" no TCC final, nem a nota do Projeto de Pesquisa.
- Pôr pré-textuais (capa, folha de rosto, resumo, listas) no sumário.
- Pôr o subtítulo em negrito.
- Fazer mais de uma rodada de perguntas.
- Citar o item 4.1.9 do manual ou qualquer origem fora de `references/`.
