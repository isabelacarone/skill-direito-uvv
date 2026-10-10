# Resultados da validação

Preencher só a partir de uma rodada real dos casos. Por pedido da autora (2026-10-09), a rodada abaixo foi feita por Claude (agente que seguiu só o SKILL.md e o references/, sem ler o Esperado antes), e não numa sessão da própria autora; cada linha diz isso na Observação. Nunca marcar `passou` sem uma rodada. Caso que falha vira correção em SKILL.md ou references/ e é repetido. Resultado válido: `pendente`, `passou` ou `falhou`; Data em AAAA-MM-DD sempre que o Resultado não for `pendente`. O histórico de falha e repetição vai na Observação.

| Caso | Arquivo | Data | Resultado | Observação |
|---|---|---|---|---|
| 1 | `tests/revisar/caso-01-citacao-longa.md` | 2026-10-09 | passou | Ajustes necessários; chamada (Streck, 2017, p. 25). Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 2 | `tests/revisar/caso-02-apud-invertido.md` | 2026-10-09 | passou | Crítico; apud corrigido sem página inventada para Freire. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 3 | `tests/formatar/caso-05-lei-acordao-soltos.md` | 2026-10-09 | passou | Lei entregue; acórdão retido com pergunta única; sem os dados, saiu com [Inserir relator] e [Inserir data de julgamento]. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 4 | `tests/revisar/caso-03-afirmacao-sem-fonte.md` | 2026-10-09 | passou | Crítico; [Inserir autor, ano, p.]; linha extra de CUR-01 aceita, não exigida. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 5 | `tests/revisar/caso-06-primeira-pessoa.md` | 2026-10-09 | passou | Ajustes necessários; 1ª pessoa e 2 frases apontadas. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 6 | `tests/revisar/caso-04-sem-secao.md` | 2026-10-09 | passou | Só a pergunta de seção e tipo de documento. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 7 | `tests/checar/caso-01-margem-fonte.md` | 2026-10-09 | passou | Script rodado de verdade: 2 ✘ (GRA-03, GRA-09), saída idêntica ao Esperado. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
| 8 | `tests/revisar/caso-05-fora-do-manual.md` | 2026-10-09 | passou | não consta no manual UVV, sem página. Rodada por Claude (agente) a pedido da autora, não em sessão dela; páginas citadas conferidas com manual_paginas.py. |
