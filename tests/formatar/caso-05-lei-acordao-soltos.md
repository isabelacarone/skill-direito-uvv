# Caso 05 - lei e acórdão do STF soltos

## Entrada

Pedido: "Formate estas duas referências." Dados soltos, fora do padrão, tirados dos exemplos do manual.

(a) Lei nº 12.092, de 21 de dezembro de 2006, do município de Curitiba. Estima a receita e fixa a despesa do município de Curitiba para o exercício financeiro de 2007. Publicada pela Câmara Municipal de Curitiba em 2007. Link: <http://domino.cmc.pr.gov.br/contlei.nsf/98454e416897038b052568fc004fc180/e5df879ac6353e7f032572800061df72>, acessado em 2 de julho de 2019.

(b) Acórdão do Supremo Tribunal Federal, 2. Turma, Recurso Extraordinário 313060/SP. Ementa: Leis 10.927/91 e 11.262 do município de São Paulo. Seguro obrigatório contra furto e roubo de automóveis. Shopping centers, lojas de departamento, supermercados e empresas com estacionamento para mais de cinquenta veículos. Inconstitucionalidade. Recorrente: Banco do Estado de São Paulo S/A – BANESPA. Recorrido: Município de São Paulo. Disponível em http://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=AC&docID=260670, acesso em 19 de agosto de 2011.

## Esperado

(a) A referência da lei, idêntica ao exemplo de REF-32:

```
CURITIBA. Lei nº 12.092, de 21 de dezembro de 2006. Estima a receita e fixa a despesa do município de Curitiba para o exercício financeiro de 2007. Curitiba: Câmara Municipal, 2007. Disponível em: http://domino.cmc.pr.gov.br/contlei.nsf/98454e416897038b052568fc004fc180/e5df879ac6353e7f032572800061df72. Acesso em: 2 jul. 2019.
```

`Regra aplicada: Manual 6.3.11, p. 66; Manual 6.3.1.6, p. 58–59; Decisão da autora`. `Ajustes nos dados:` jurisdição CURITIBA deduzida de "do município de Curitiba"; editor "Câmara Municipal de Curitiba" reduzido a `Curitiba: Câmara Municipal` porque o local já está dado (como no exemplo do manual); link sem `< >`; "acessado em" virou `Acesso em:`; data de acesso "2 de julho de 2019" virou `2 jul. 2019`.

(b) O acórdão não é entregue ainda. A skill faz uma pergunta única: qual o nome do relator ou da relatora e qual a data de julgamento (REF-69: relator e data de julgamento são obrigatórios). A pergunta não pede link, data de acesso nem outro campo, que já foram fornecidos.

Se a autora responder "Min. Ellen Gracie" e "29 de novembro de 2005", o acórdão sai idêntico ao exemplo de REF-35:

```
BRASIL. Supremo Tribunal Federal (2. Turma). Recurso Extraordinário 313060/SP. Leis 10.927/91 e 11.262 do município de São Paulo. Seguro obrigatório contra furto e roubo de automóveis. Shopping centers, lojas de departamento, supermercados e empresas com estacionamento para mais de cinquenta veículos. Inconstitucionalidade. Recorrente: Banco do Estado de São Paulo S/A – BANESPA. Recorrido: Município de São Paulo. Relatora: Min. Ellen Gracie, 29 de novembro de 2005. Disponível em: http://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=AC&docID=260670. Acesso em: 19 ago. 2011.
```

`Regra aplicada: Manual 6.3.12, p. 66; Manual 6.3.12, p. 67`. `Ajustes nos dados:` jurisdição BRASIL deduzida do Supremo Tribunal Federal; "Disponível em" ganhou dois-pontos; "acesso em" virou `Acesso em:`; data de acesso "19 de agosto de 2011" virou `19 ago. 2011`; link sem `< >` quando houver; a ementa foi transcrita como fornecida.

## Não pode

- Inventar relator, data de julgamento, número do processo, turma ou ementa.
- Resumir, completar ou reescrever a ementa.
- `< >` no link.
- Entregar o acórdão antes de a autora informar relator(a) e data de julgamento.
- Perguntar por link, data de acesso ou outro campo já fornecido.
