import streamlit as st
from google import genai

# =========================
# 1. Configuração Visual
# =========================
st.set_page_config(page_title="Suporte Seu Arnaldo", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #fdf5e6; }
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
        text-align: center;
    }
    </style>
    <div class="header-container">
        <h1>🍔 ARNALDO BURGERS</h1>
        <p>SISTEMA DE ATENDIMENTO AO PARCEIRO</p>
    </div>
    <div class="status-bar">
        ⏳ ABERTURA DA LOJA EM: 28:15 | Status: Seu Arnaldo está Ansioso
    </div>
""", unsafe_allow_html=True)

# =========================
# 2. Inicialização da API
# =========================
try:
    client = genai.Client(api_key=st.secrets["MINHA_CHAVE"])
except Exception as e:
    st.error("Erro ao configurar API. Verifique a chave nos Secrets.")
    st.stop()

SYSTEM_PROMPT = """
Aja como o 'Seu Arnaldo', dono de uma hamburgueria de bairro.
Você é simples, pouco tecnológico e está com pressa.
Não entende termos técnicos (setup, dashboard, interface).
Responda de forma curta, direta e informal, como se fosse no WhatsApp.
"""

# =========================
# 3. Gestão do Histórico
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []
    msg_inicial = """Oi, boa tarde! Moço(a), eu estou aqui tentando mexer nesse cardápio novo que eu assinei, mas olha... tá difícil. Eu já coloquei o X-Salada, mas não acho onde que eu coloco pro cliente escolher se quer tirar a cebola ou se quer pagar mais 5 reais pra vir com bacon dobrado. E a pizza de dois sabores? Como faz? Me ajuda aí que o movimento já vai começar!"""
    st.session_state.messages.append({"role": "assistant", "content": msg_inicial})

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 4. Lógica de Resposta
# =========================
if prompt := st.chat_input("Responda ao Seu Arnaldo..."):
    
    # Mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Monta contexto completo
        contexto_completo = f"Instrução de Personagem:\n{SYSTEM_PROMPT}\n\n"

        for m in st.session_state.messages:
            if m["role"] == "assistant":
                contexto_completo += f"Seu Arnaldo: {m['content']}\n"
            else:
                contexto_completo += f"Analista: {m['content']}\n"

        contexto_completo += "\nSeu Arnaldo responda ao analista:\n"

        # Chamada para Gemini
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contexto_completo,
        )

        resposta_texto = response.text

        if resposta_texto:
            st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
            with st.chat_message("assistant"):
                st.markdown(resposta_texto)

    except Exception as e:
        st.error(f"Erro na resposta: {e}")
