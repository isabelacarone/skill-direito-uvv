# Caso 02 - citação direta sem página

## Entrada

Pedido: "Monte uma citação direta curta de Canuto (1999), com o trecho: [...] surgiu de uma paixão incontrolável." Sem página informada.

## Esperado

- A skill pede a página, e só ela, numa única mensagem, e não entrega a chamada.
- Se a autora responder que não tem a página, entrega a citação com o marcador no lugar, e diz que a citação direta exige página (Manual 4.1.1, p. 36):

```
Canuto (1999, p. [Inserir página]) afirma que seu trabalho “[...] surgiu de uma paixão incontrolável”.
```

- Diz que a forma de indicar dado ausente "não consta no manual UVV", cita a NBR 10520:2023 só como orientação geral, sem página, e sugere a Biblioteca Central.
- `Regra aplicada:` com origem copiada de `references/citacoes.md`.

## Não pode

- Gerar `p. 15` ou qualquer outra página.
- Entregar a citação antes de perguntar.
- Pedir os dados em mais de uma mensagem.
- Citar página da NBR.
