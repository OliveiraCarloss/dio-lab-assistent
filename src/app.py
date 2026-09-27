import streamlit as st
from agente import gerar_resposta
from config import NOME_AGENTE

st.set_page_config(page_title=NOME_AGENTE, page_icon="📈")

st.title(f"📈 {NOME_AGENTE}")
st.caption("Seu guia de investimentos de longo prazo (horizonte mínimo de 5 anos)")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": (
                f"Olá! Eu sou o {NOME_AGENTE}, seu guia de investimentos de longo prazo. "
                "Estou aqui pra te ajudar a entender onde e por que investir pensando lá na frente. "
                "O que você gostaria de saber?"
            ),
        }
    ]

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua pergunta sobre investimentos...")

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = gerar_resposta(st.session_state.mensagens)
            st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
