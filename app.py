import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["MINHA_CHAVE"])

models = client.models.list()

for m in models:
    st.write(m.name)
