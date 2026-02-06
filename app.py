import streamlit as st
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Simulador de Atendimento - Goomer", layout="centered")
st.title("🍔 Teste Prático: Atendimento Goomer")
st.info("Cenário: Você está atendendo o Seu Arnaldo (Arnaldo Burgers). Resolva as dúvidas dele usando a Central de Ajuda.")

# Configurar a API (Substitua pela sua chave ou use Secrets do Streamlit)
genai.configure(api_key=st.secrets["AIzaSyD_t4b0g2j8vONUIsnf-Zaqj0_h21g4loo"])

# Instruções secretas da Persona
SYSTEM_PROMPT = """
Você é o "Seu Arnaldo", dono da "Arnaldo Burgers". Você é um pequeno empresário, pouco tecnológico e está com pressa.
Você não entende termos técnicos (setup, UI, dashboard). Se o analista usar esses termos, reclame.
Dúvidas: 1. Adicionais no X-Salada (bacon extra). 2. Pizza meio a meio (cobrar a mais cara).
Seja educado, mas ansioso. Só dê o atendimento como concluído se o analista explicar o passo a passo de forma simples.
Primeira mensagem: "Oi, boa tarde! Moço(a), eu estou aqui tentando mexer nesse cardápio novo, mas olha... tá difícil. Eu já coloquei o X-Salada, mas não acho onde que eu coloco pro cliente escolher se quer tirar a cebola ou se quer pagar mais 5 reais pra vir com bacon dobrado. E a pizza de dois sabores? Como faz? Me ajuda aí que o movimento já vai começar!"
"""

# Inicializar o modelo
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem inicial do Seu Arnaldo
    initial_msg = "Oi, boa tarde! Moço(a), eu estou aqui tentando mexer nesse cardápio novo, mas olha... tá difícil. Eu já coloquei o X-Salada, mas não acho onde que eu coloco pro cliente escolher se quer tirar a cebola ou se quer pagar mais 5 reais pra vir com bacon dobrado. E a pizza de dois sabores? Como faz? Me ajuda aí que o movimento já vai começar!"
    st.session_state.messages.append({"role": "assistant", "content": initial_msg})

# Exibir mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do Analista
if prompt := st.chat_input("Digite sua resposta aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Seu Arnaldo
    with st.chat_message("assistant"):
        full_history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
        response = model.generate_content(full_history)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
