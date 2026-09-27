# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Utilização no Agente |
|---------|---------|------------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores com o cliente |
| `perfil_investidor.json` | JSON | Personalizar exemplos e explicações conforme o perfil do cliente |
| `conceitos_financeiros.json` | JSON | Base de conhecimento sobre categorias de investimento, juros compostos e horizonte de longo prazo |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente, usado como exemplo prático nas explicações |

---
---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim. Mantive a estrutura original dos arquivos, mas ajustei o conteúdo para refletir o foco do agente em investimentos de longo prazo:

- `perfil_investidor.json`: troquei o objetivo principal e uma das metas por um objetivo de longo prazo (independência financeira/aposentadoria), para servir de exemplo real de horizonte de 5+ anos.
- `produtos_financeiros.json`: substituí o campo `indicado_para` por `contexto_educativo`, removendo qualquer linguagem de recomendação personalizada de compra, já que o agente não sugere ativos específicos.
- `historico_atendimento.csv`: atualizei os temas de atendimento para refletir dúvidas típicas de um cliente com foco em longo prazo (juros compostos, volatilidade, horizonte de investimento).
- `transacoes.csv`: mantido como no template original, usado como exemplo de análise de padrão de gastos.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.


````python
import pandas as pd
import json

# CSVs
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')

# JSONs
with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)

with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)
````

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

-- Optei por injetar os dados diretamente como texto dentro do system prompt, cada um precedido de um cabeçalho que identifica a origem do dado

```text
### PERFIL DO CLIENTE (fonte: perfil_investidor.json)
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir patrimônio no longo prazo",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "horizonte_investimento": "longo prazo (mínimo 5 anos)",
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Independência financeira / aposentadoria",
      "valor_necessario": 500000.00,
      "prazo": "2041-12"
    }
  ]
}

### HISTÓRICO DE TRANSAÇÕES (fonte: transacoes.csv)
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

### HISTÓRICO DE ATENDIMENTO (fonte: historico_atendimento.csv)
data,canal,tema,resumo,resolvido
2025-09-15,chat,Investimento de longo prazo,Cliente perguntou por que vale a pena esperar mais de 5 anos para ver resultado,sim
2025-09-22,chat,Juros compostos,Cliente teve dúvida sobre como o rendimento cresce com o tempo,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto como exemplo de reserva de emergência,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência e da meta de longo prazo,sim
2025-10-25,chat,Volatilidade de mercado,Cliente perguntou se deveria vender após queda no mercado e foi orientado sobre horizonte de longo prazo,sim

### CATEGORIAS DE INVESTIMENTO (fonte: produtos_financeiros.json)
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "contexto_educativo": "Costuma ser usado como exemplo de reserva de emergência por ter liquidez e baixo risco"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "contexto_educativo": "Exemplo de renda fixa com liquidez diária, útil para entender rendimento previsível"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "contexto_educativo": "Exemplo de investimento isento de IR, mas com prazo de carência — bom pra explicar liquidez"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "contexto_educativo": "Exemplo de diversificação entre classes de ativos, comum em carteiras de longo prazo"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "contexto_educativo": "Exemplo de investimento de maior risco, cuja volatilidade tende a se equilibrar apenas em horizontes longos (5+ anos)"
  }
]
```

---

# Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Idade: 32 anos | Profissão: Analista de Sistemas
- Perfil de investidor: Moderado (não aceita alto risco)
- Renda mensal: R$ 5.000,00
- Patrimônio total: R$ 15.000,00
- Reserva de emergência atual: R$ 10.000,00
- Objetivo principal: Construir patrimônio no longo prazo
- Horizonte de investimento: Longo prazo (mínimo 5 anos)

Metas:
- Completar reserva de emergência: R$ 15.000,00 até 06/2026
- Independência financeira / aposentadoria: R$ 500.000,00 até 12/2041

Últimas transações:
- 01/10: Salário - R$ 5.000,00 (entrada)
- 02/10: Aluguel - R$ 1.200,00 (saída)
- 03/10: Supermercado - R$ 450,00 (saída)
- 12/10: Uber - R$ 45,00 (saída)
- 25/10: Combustível - R$ 250,00 (saída)

Histórico de atendimento:
- 15/09: Dúvida sobre por que esperar 5+ anos traz melhores resultados
- 22/09: Dúvida sobre como juros compostos funcionam ao longo do tempo
- 25/10: Perguntou se deveria vender após queda no mercado
```
