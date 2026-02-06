import streamlit as st
import google.generativeai as genai

# 1. Configuração Visual (Estilo AI Studio)
st.set_page_config(page_title="Suporte Seu Arnaldo", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #fdf5e6; }
    .stChatInputContainer { padding-bottom: 20px; }
    .header-container {
        background-color: #b30000;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .status-bar {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffeeba;
        margin-bottom: 20px;
        font-weight: bold;
    }
    </style>
    <div class="header-container">
        <h1>🍔 ARNALDO BURGERS</h1>
        <p>HAMBURGUERIA & PIZZARIA</p>
    </div>
    <div class="status-bar">
        ⏳ ABERTURA EM: 29:53 | Status do Arnaldo: Desesperado
    </div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Objetivo da Chamada (Apenas para o Analista)", expanded=True):
    st.markdown("""
    * Explicar como adicionar **'Bacon Extra'** (Adicionais/Complementos).
    * Explicar como configurar **Pizza Meio a Meio** (Preço da mais cara).
    * **Aviso:** Evite termos técnicos ou inglês. Seu Arnaldo não gosta!
    """)

# 2. Configuração da API
try:
    genai.configure(api_key=st.secrets["MINHA_CHAVE"])
except:
    st.error("Erro na Chave de API. Verifique os Secrets.")

SYSTEM_PROMPT = """
Aja como o 'Seu Arnaldo', dono da 'Arnaldo Burgers'. Você é pouco tecnológico e está ansioso.
Não aceite termos como 'setup', 'dashboard', 'interface'.
Objetivos: Adicionais no X-Salada e Pizza Meio a Meio.
Responda de forma curta e direta, como alguém que está no meio da cozinha.
"""

# Usando o modelo estável para evitar o erro NotFound
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# 3. Lógica do Chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    
    # Mensagem inicial manual para garantir que apareça com o estilo certo
    msg_inicial = "Oi, boa tarde! Moço(a), eu estou aqui tentando mexer nesse cardápio novo, mas olha... tá difícil. Eu já coloquei o X-Salada, mas não acho onde que eu coloco pro cliente escolher se quer tirar a cebola ou se quer pagar mais 5 reais pra vir com bacon dobrado. E a pizza de dois sabores? Como faz? Me ajuda aí que o movimento já vai começar!"
    st.session_state.messages.append({"role": "assistant", "content": msg_inicial})

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Explique para o Seu Arnaldo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Envia a mensagem e recebe a resposta do modelo
        response = st.session_state.chat.send_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
