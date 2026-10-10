# Caso 04 - arquivo inexistente

## Entrada

Pedido: "Cheque C:/pasta-de-teste/nao-existe.docx"

## Esperado

- A skill roda o script, que sai com código 2, mostra a mensagem do script como veio (`Não foi possível ler o arquivo: arquivo não encontrado`) e pede o caminho certo ou o próprio .docx.
- Não monta relatório.

## Não pode

- Montar relatório ou tabela de ✔ e ✘.
- Presumir a formatação do documento.
- Procurar o arquivo por outro meio ou abrir outro .docx.
