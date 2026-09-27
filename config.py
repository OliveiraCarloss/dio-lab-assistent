# Configurações gerais do agente "Futuro não tão Distante"

import os

# Modelo Ollama utilizado. Optei pelo "llama3.2:1b" por ser um modelo leve,
# adequado para rodar em máquinas com hardware mais modesto (poucos recursos
# de RAM/GPU), mantendo qualidade suficiente para respostas educativas.
OLLAMA_MODEL = "llama3.2:1b"

# Caminho absoluto até a raiz do projeto, independente de onde o comando
# "streamlit run" for executado (evita erro de "arquivo não encontrado")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

PERFIL_PATH = os.path.join(DATA_DIR, "perfil_investidor.json")
PRODUTOS_PATH = os.path.join(DATA_DIR, "produtos_financeiros.json")
TRANSACOES_PATH = os.path.join(DATA_DIR, "transacoes.csv")
HISTORICO_PATH = os.path.join(DATA_DIR, "historico_atendimento.csv")

# Nome de exibição do agente na interface
NOME_AGENTE = "Futuro não tão Distante"
