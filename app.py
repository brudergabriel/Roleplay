import streamlit as st
import google.generativeai as genai

# 1. Configuração Visual
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

# 2. Inicialização da API
try:
    genai.configure(api_key=st.secrets["MINHA_CHAVE"])
except Exception as e:
    st.error("Erro nos Secrets: Verifique a chave MINHA_CHAVE.")

SYSTEM_PROMPT = """Aja como o 'Seu Arnaldo', dono de uma hamburgueria de bairro. 
Você é simples, pouco tecnológico e está com pressa. 
Não entende termos técnicos (setup, dashboard, interface). 
Responda de forma curta e direta, como se fosse no WhatsApp."""

# Alteração para o modelo 'gemini-pro', que é mais compatível com a v1beta atual
model = genai.GenerativeModel(model_name='gemini-pro')

# 3. Gestão do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []
    msg_inicial = """Oi, boa tarde! Moço(a), eu estou aqui tentando mexer nesse cardápio novo que eu assinei, mas olha... tá difícil. Eu já coloquei o X-Salada, mas não acho onde que eu coloco pro cliente escolher se quer tirar a cebola ou se quer pagar mais 5 reais pra vir com bacon dobrado. E a pizza de dois sabores? Como faz? Me ajuda aí que o movimento já vai começar!"""
    st.session_state.messages.append({"role": "assistant", "content": msg_inicial})

# Exibir mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Lógica de Resposta
if prompt := st.chat_input("Responda ao Seu Arnaldo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Criando o prompt contextulizado para o modelo
        contexto_completo = f"Instrução de Personagem: {SYSTEM_PROMPT}\n\n"
        for m in st.session_state.messages:
            prefixo = "Cliente (Seu Arnaldo):" if m["role"] == "assistant" else "Analista:"
            contexto_completo += f"{prefixo} {m['content']}\n"
        
        contexto_completo += "\nSeu Arnaldo responda ao analista:"

        response = model.generate_content(contexto_completo)
        
        if response.text:
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
    except Exception as e:
        st.error(f"Erro na resposta: {e}")
