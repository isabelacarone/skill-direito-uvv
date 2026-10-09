# Caso 01 - as quatro citações a partir de dados completos

## Entrada

Pedido: "Monte estas quatro citações no padrão UVV." Dados dos exemplos do manual (a ideia do item 3 é fictícia, só para o teste).

1. Citação direta curta. Autor: Canuto. Ano: 1999. Página: 15. Trecho: "[...] surgiu de uma paixão incontrolável". Autor na frase.
2. Citação indireta. Autor: Gonçalves. Ano: 2019. Ideia: o estudo do tema avançou na última década. Autor entre parênteses.
3. Citação de citação (apud), indireta. Autor original: Cagliari, 1986, p. 104. Lido em: Suassuba, 1995, p. 55. Ideia: a leitura precede a escrita na alfabetização.
4. Citação direta longa. Autor: França. Ano: 2003. Página: 30. Trecho: "Dentre os trabalhos monográficos mais usuais, destacam-se aqueles exigidos para obtenção de graus, como a dissertação de mestrado e a tese de doutorado. Para a conclusão de cursos de especialização, ou mesmo de graduação, é comum apresentação de trabalhos acadêmicos muitas vezes chamados simplesmente de monografias".

## Esperado

Quatro blocos de código, nesta ordem, cada um seguido de `Regra aplicada:` com a origem copiada de `references/citacoes.md`.

1. Curta:

```
Canuto (1999, p. 15) afirma que seu trabalho “[...] surgiu de uma paixão incontrolável”.
```

`Regra aplicada: Manual 4.1.2, p. 36; Manual 4.4.8, p. 45–46`

2. Indireta, sem página:

```
O estudo do tema avançou na última década (Gonçalves, 2019).
```

`Regra aplicada: Manual 4.2, p. 39; Manual 4.4.7, p. 45`

3. Apud, autor original primeiro:

```
A leitura precede a escrita na alfabetização (Cagliari, 1986, p. 104 apud Suassuba, 1995, p. 55).
```

`Regra aplicada: Manual 4.3, p. 39–40`. Avisa que na lista de referências entra só Suassuba (1995).

4. Longa, sem aspas:

```
Dentre os trabalhos monográficos mais usuais, destacam-se aqueles exigidos para obtenção de graus, como a dissertação de mestrado e a tese de doutorado. Para a conclusão de cursos de especialização, ou mesmo de graduação, é comum apresentação de trabalhos acadêmicos muitas vezes chamados simplesmente de monografias (França, 2003, p. 30).
```

`Regra aplicada: Manual 4.1.3, p. 37`. Linha `Formatação no Word:` com parágrafo isolado, recuo de 4 cm, Arial 10, espaçamento simples, sem aspas. O trecho tem cerca de 330 caracteres, dentro do limite de 10 linhas, então não leva o aviso; se levar, diz que a contagem é estimativa e vale no Word.

## Não pode

- Sobrenome em maiúsculas na chamada.
- Aspas na citação longa.
- Página na citação indireta de Gonçalves.
- Origem fora de `references/` ou escrita de memória.
- Mudar o trecho ou qualquer dado sem declarar em `Ajustes nos dados:`.
- Inverter o apud (Suassuba antes de Cagliari).
