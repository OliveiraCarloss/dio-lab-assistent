import json
import pandas as pd
import ollama

from config import (
    OLLAMA_MODEL,
    PERFIL_PATH,
    PRODUTOS_PATH,
    TRANSACOES_PATH,
    HISTORICO_PATH,
)

SYSTEM_PROMPT_BASE = """
Você é o "Futuro não tão Distante", um agente educativo especializado em investimentos de longo prazo (horizonte mínimo de 5 anos).

Seu objetivo é ajudar o cliente a entender os fundamentos por trás de decisões financeiras de longo prazo, por que a paciência e a consistência importam mais do que tentar acertar o timing do mercado, como funcionam os juros compostos, e quais categorias de investimento costumam fazer sentido em diferentes perfis de risco.

PERSONALIDADE:
- Calmo e ponderado: nunca cria senso de urgência. Se o cliente demonstrar ansiedade (ex: querer vender após uma queda do mercado), traga a conversa de volta para o horizonte de longo prazo.
- Didático, não professoral: explique conceitos complexos de forma simples, sem soar como aula chata nem menosprezar o conhecimento do cliente.
- Direto e honesto: nunca prometa rentabilidade, nunca crie senso de "oportunidade única".
- Paciente: trate perguntas repetidas ou básicas com a mesma disposição.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos no contexto (perfil do cliente, transações e histórico de atendimento) e nos conceitos de investimento disponíveis.
2. Nunca invente números, rentabilidades ou informações financeiras que não estejam no contexto fornecido.
3. NUNCA recomende a compra ou venda de um ativo específico, mesmo que o cliente insista. Explique o motivo da limitação e ofereça uma explicação educativa sobre a categoria do ativo em questão.
4. Sempre reforce o horizonte de investimento de longo prazo (mínimo 5 anos), especialmente quando o cliente demonstrar ansiedade com volatilidade de curto prazo.
5. Use os dados do cliente apenas como exemplo prático para ilustrar conceitos, nunca como base para uma recomendação personalizada de investimento.
6. Se não souber algo ou o tema estiver fora do seu escopo, admita a limitação claramente e sugira que o cliente busque um profissional habilitado.
7. Não utilize dados de mercado em tempo real, suas explicações são baseadas em conceitos gerais, não em cotações atuais.
8. Mantenha respostas objetivas e evite jargão técnico sem explicação.
""".strip()


def carregar_dados():
    """Carrega os arquivos da pasta data e retorna como dicionário."""
    with open(PERFIL_PATH, "r", encoding="utf-8") as f:
        perfil = json.load(f)

    with open(PRODUTOS_PATH, "r", encoding="utf-8") as f:
        produtos = json.load(f)

    transacoes = pd.read_csv(TRANSACOES_PATH)
    historico = pd.read_csv(HISTORICO_PATH)

    return {
        "perfil": perfil,
        "produtos": produtos,
        "transacoes": transacoes,
        "historico": historico,
    }


def formatar_contexto(dados):
    """Transforma os dados carregados em texto legível para o system prompt."""
    perfil = dados["perfil"]
    transacoes = dados["transacoes"].tail(5)
    historico = dados["historico"].tail(3)

    metas_texto = "\n".join(
        f"- {m['meta']}: R$ {m['valor_necessario']:,.2f} até {m['prazo']}"
        for m in perfil["metas"]
    )

    transacoes_texto = "\n".join(
        f"- {row['data']}: {row['descricao']} - R$ {row['valor']:,.2f} ({row['tipo']})"
        for _, row in transacoes.iterrows()
    )

    historico_texto = "\n".join(
        f"- {row['data']}: {row['resumo']}"
        for _, row in historico.iterrows()
    )

    contexto = f"""
Dados do Cliente:
- Nome: {perfil['nome']}
- Idade: {perfil['idade']} anos | Profissão: {perfil['profissao']}
- Perfil de investidor: {perfil['perfil_investidor']}
- Renda mensal: R$ {perfil['renda_mensal']:,.2f}
- Patrimônio total: R$ {perfil['patrimonio_total']:,.2f}
- Reserva de emergência atual: R$ {perfil['reserva_emergencia_atual']:,.2f}
- Objetivo principal: {perfil['objetivo_principal']}
- Horizonte de investimento: {perfil['horizonte_investimento']}

Metas:
{metas_texto}

Últimas transações:
{transacoes_texto}

Histórico de atendimento recente:
{historico_texto}
""".strip()

    return contexto


def montar_system_prompt():
    dados = carregar_dados()
    contexto = formatar_contexto(dados)
    return f"{SYSTEM_PROMPT_BASE}\n\nCONTEXTO DO CLIENTE:\n{contexto}"


def gerar_resposta(mensagens_usuario):
    """
    mensagens_usuario: lista de dicionários no formato do histórico de chat do Streamlit,
    ex: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    system_prompt = montar_system_prompt()

    mensagens = [{"role": "system", "content": system_prompt}] + mensagens_usuario

    try:
        resposta = ollama.chat(model=OLLAMA_MODEL, messages=mensagens)
        return resposta["message"]["content"]
    except Exception as e:
        return (
            "Não consegui me conectar ao modelo local. Verifique se o Ollama está "
            f"rodando e se o modelo '{OLLAMA_MODEL}' foi baixado (`ollama pull {OLLAMA_MODEL}`).\n\n"
            f"Detalhe técnico: {e}"
        )
