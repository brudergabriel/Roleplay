import streamlit as st
import google.generativeai as genai

# 1. Configuração Visual Estilizada
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

with st.expander("ℹ️ INSTRUÇÕES DO TESTE (Para o Analista)", expanded=False):
    st.markdown("""
    **Cenário:** O Seu Arnaldo é um cliente VSB que não entende de tecnologia.
    **Sua Missão:** 1. Explique como configurar **Adicionais** (Bacon Extra).
    2. Explique como configurar **Pizza Meio a Meio** (Preço da mais cara).
    **Regra:** Não use termos técnicos em inglês. Seja simples e paciente.
    """)

# 2. Inicialização da API
try:
    genai.configure(api_key=st.secrets["MINHA_CHAVE"])
except Exception as e:
    st.error("Erro nos Secrets: Verifique se 'MINHA_CHAVE' está configurada no Streamlit Cloud.")

# Configuração do Modelo
SYSTEM_PROMPT = (
    "Aja como o 'Seu Arnaldo', dono de uma hamburgueria de bairro. Você é simples, pouco tecnológico e está com pressa. "
    "Não entende palavras como setup, dashboard, interface ou UI. Se usarem, reclame. "
    "Você quer saber sobre adicionais e pizza de dois sabores. Responda de forma curta, como no WhatsApp."
)

model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# 3. Gestão do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem Inicial
    msg_inicial = "Oi, boa tarde! Moço(a), eu estou aqui tentando mexer nesse cardápio novo, mas olha...
