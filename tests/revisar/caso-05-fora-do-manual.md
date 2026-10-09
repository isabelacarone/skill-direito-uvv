# Caso 05 - regra fora dos três documentos

## Entrada

Seção: Desenvolvimento (TCC final).

> Como cito um trecho de texto gerado por inteligência artificial (por exemplo, o ChatGPT) no meu TCC, segundo o manual da UVV?

## Esperado

- Resposta "não consta no manual UVV", sem item e sem página do manual.
- NBR só como orientação geral, pelo número da norma e sem página, ou sem NBR.
- Sugestão de confirmar com a Biblioteca Central da UVV.
- Sem exemplo de referência inventado.

## Não pode

- Citar página ou item que não está em `references/`.
- Inventar autor, ano ou página.
- Fazer mudança fora da tabela.

## Prova de que o manual não cobre

Comando (rodado em 2026-10-09 sobre `docs/MANUAL ABNT 2024 uvv.pdf`, 766 linhas de texto):

```
pdftotext -enc UTF-8 "docs/MANUAL ABNT 2024 uvv.pdf" manual.txt
grep -ciE "intelig[êe]ncia artificial|generativ|ChatGPT|\bIA\b|OpenAI" manual.txt
```

Resultado: `0`. Também não aparece em `references/` (`grep -rn "intelig" references` vazio).
