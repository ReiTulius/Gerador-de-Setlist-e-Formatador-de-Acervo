import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Configuração da página do aplicativo (Definida apenas UMA vez no topo do site)
st.set_page_config(page_title="Painel Udesc FM - Tulio", page_icon="📻", layout="wide")

# 🔗 LINK DA PLANILHA DO GOOGLE DO TEU GERADOR DE SETLIST
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1zkPm3F9W8QbOBhKvdV7jFCYqH-U8Qbru5w5TDyAHQLw/edit?usp=sharing"

# --- MENU LATERAL DE NAVEGAÇÃO ---
st.sidebar.title("📻 Painel de Controle")
st.sidebar.markdown("Escolha a ferramenta que deseja usar agora:")
opcao = st.sidebar.radio(
    "Navegar para:",
    ["💿 Formatador de Acervo", "📸 Gerador de Setlist (Instagram)"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para otimizar a programação da Udesc FM 🎧")


# ==========================================
# FUNÇÕES DE SUPORTE DO GERADOR DE SETLIST
# ==========================================
def converter_link_google(url):
    if "docs.google.com/spreadsheets" in url:
