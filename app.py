import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Configuração da página do aplicativo (Definida apenas UMA vez no topo)
st.set_page_config(page_title="Painel Udesc FM - Tulio", page_icon="📻", layout="wide")

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
# FUNÇÕES DE SUPORTE
# ==========================================
def processar_linha_musica(linha_bruta):
    linha_original = linha_bruta.strip().replace('"', '')
    if not line_original:
        return None
        
    # IDENTIFICAÇÃO DE SC
    linha_limpa_fim = linha_original.lower()
    if linha_limpa_fim.endswith(".mp3"):
        linha_limpa_fim = linha_limpa_fim[:-4].strip()
        
    eh_sc = False
    if linha_limpa_fim.endswith("- sc") or linha_limpa_fim.endswith("-sc"):
        eh_sc = True
        
    # LIMPEZA PADRÃO
    if "\\" in linha_original:
        linha_trabalho = linha_original.split("\\")[-1]
    else:
        linha_trabalho = linha_original
        
    if linha_trabalho.lower().endswith(".mp3"):
        linha_trabalho = linha_trabalho[:-4]
        
    if eh_sc:
        linha_trabalho = re.sub(r'\s*-\s*sc\s*$', '', linha_trabalho, flags=re.IGNORECASE).strip()
        
    artista = ""
    participacao = ""
    musica = ""
    formato = ""
    ano = ""
    compositores = ""
    
    padrao_comp = r'\((comp\.|compa)[^)]+\)'
    busca_comp = re.search(padrao_comp, linha_trabalho, flags=re.IGNORECASE)
    
    if busca_comp:
        compositores_com_parentese = busca_comp.group(0)
        compositores = re.sub(r'\((comp\.|compa)\s*', '', compositores_com_parentese, flags=re.IGNORECASE).rstrip(')')
        linha_trabalho = linha_trabalho.replace(compositores_com_parentese, "").replace("  ", " ")
    else:
        linha_trabalho = linha_trabalho

    partes = [p.strip() for p in linha_trabalho.split(" - ")]
    
    if len(partes) < 2:
        return None
        
    artista = partes[0]
    
    indice_atual = 1
    if indice_atual < len(partes) and ("part." in partes[indice_atual].lower() or "part " in partes[indice_atual].lower()):
        participacao = re.sub(r'\(?part\.?\s*', '', partes[indice_atual], flags=re.IGNORECASE).rstrip(')')
        indice_atual += 1
        
    if indice_atual < len(partes):
        musica = partes[indice_atual]
        indice_atual += 1
        
    if indice_atual < len(partes):
        if indice_atual == len(partes) - 1 and partes[indice_atual].isdigit():
            pass
        else:
            formato = partes[indice_atual]
            indice_atual += 1
            
    if len(partes) > indice_atual and partes[-1].isdigit():
        ano = partes[-1]

    part_str = f" - (part. {participacao})" if participacao else ""
    comp_str = f" (comp. {compositores})" if compositores else ""
    formato_str = f" - {formato}" if formato else ""
    ano_str = f" - {ano}" if ano else ""
    sc_str = " - SC" if eh_sc else ""
    
    nome_arquivo_formatado = f"{artista}{part_str} - {musica}{comp_str}{formato_str}{ano_str}{sc_str}"
    nome_arquivo_formatado = re.sub(r'\s+', ' ', nome_arquivo_formatado).strip()

    return {
        "eh_sc": eh_sc,
        "Música": musica,
        "Artista": artista,
        "Compositores": compositores,
        "Formato": formato,
        "Ano": ano,
        "Origem": "",
        "Gênero": "",
        "Gênero Relacionado": "",
        "Est/Idioma": "SC" if eh_sc else "",
        "Classificação": "",
        "Andamento": "",
        "Data Cadastro": datetime.now().strftime("%d/%m/%Y"),
        "Participações": participacao,
        "Nome do Arquivo": nome_arquivo_formatado
    }


# ==========================================
# PÁGINA 1: FORMATADOR DE ACERVO
# ==========================================
if opcao == "💿 Formatador de Acervo":
    st.title("💿 Automatizador de Acervo Para Udesc FM")
    st.markdown("Insira a lista de músicas para limpar, formatar e separar para o Acervo Geral ou Som da Ilha (SC).")

    texto_bruto = st.text_area("Cole aqui as linhas brutas das músicas baixadas (pode misturar normais e com SC):", height=250, placeholder="M:\\...")

    if st.button("Processar e Organizar Acervos 🚀", type="primary"):
        if texto_bruto:
            linhas = texto_bruto.split('\n')
            lista_geral = []
            lista_sc = []
            
            for linha in linhas:
                res = processar_linha_musica(linha)
                if res:
                    eh_sc = res.pop("eh_sc")
                    
                    if eh_sc:
                        dados_sc = {
                            "Música": res["Música"], "Artista": res["Artista"], "Compositores": res["Compositores"],
                            "Formato": res["Formato"], "Ano": res["Ano"], "Origem": res["Origem"], "Gênero": res["Gênero"],
                            "Gênero Relacionado": res["Gênero Relacionado"], "Est": "SC", "Classificação": res["Classificação"],
                            "Andamento": res["Andamento"], "Data Cadastro": res["Data Cadastro"], "Participações": res["Participações"],
                            "Nome do Arquivo": res["Nome do Arquivo"]
                        }
                        lista_sc.append(dados_sc)
                    else:
                        dados_geral = {
                            "Música": res["Música"], "Artista": res["Artista"], "Compositores": res["Compositores"],
                            "Formato": res["Formato"], "Ano": res["Ano"], "Origem": res["Origem"], "Gênero": res["Gênero"],
                            "Gênero Relacionado": res["Gênero Relacionado"], "Idioma": "", "Classificação": res["Classificação"],
                            "Andamento": res["Andamento"], "Data Cadastro": res["Data Cadastro"], "Participações": res["Participações"],
                            "Nome do Arquivo": res["Nome do Arquivo"]
                        }
                        lista_geral.append(dados_geral)
            
            if lista_geral:
                df_geral = pd.DataFrame(lista_geral)
                df_geral.drop_duplicates(subset=["Nome do Arquivo"], keep="first", inplace=True)
                st.success(f"🎉 {len(df_geral)} músicas prontas para o ACERVO GERAL!")
                st.markdown("👉 *Clique na tabela abaixo, use **Ctrl+A** e **Ctrl+C**, e cole na sua planilha do Acervo Geral.*")
                st.dataframe(df_geral, use_container_width=True)
                
            if lista_sc:
                df_sc = pd.DataFrame(lista_sc)
                df_sc.drop_duplicates(subset=["Nome do Arquivo"], keep="first", inplace=True)
                st.warning(f"🏝️ {len(df_sc)} músicas de Santa Catarina identificadas para o SOM DA ILHA!")
                st.markdown("👉 *Clique na tabela abaixo, use **Ctrl+A** e **Ctrl+C**, e cole na sua planilha do Som da Ilha.*")
                st.dataframe(df_sc, use_container_width=True)
                
            if lista_geral or lista_sc:
                st.balloons()
            else:
                st.warning("Nenhuma linha válida encontrada no padrão.")
        else:
            st.warning("Cole os dados antes de processar.")


# ==========================================
# PÁGINA 2: GERADOR DE SETLIST INSTAGRAM
# ==========================================
elif opcao == "📸 Gerador de Setlist (Instagram)":
    st.title("📸 Gerador de Setlist para Instagram")
    st.markdown("Cole as músicas tocadas no bloco para gerar o texto de divulgação marcando o @ dos artistas do Som da Ilha.")

    # Banco de dados de arrobas (Você pode adicionar quantos quiser aqui dentro seguindo o padrão)
    dicionario_artistas = {
        "tulio mota": "@tuliomota_",
        "jessica lourenço": "@jessicalourenco",
        "aaron frazer": "@aaron_frazer",
        "addison rae": "@addisonre"
    }

    texto_setlist = st.text_area("Cole aqui as linhas das músicas que tocaram no programa:", height=200, placeholder="Tulio Mota - Pirilampo...")

    if st.button("Gerar Texto para o Insta 📲", type="primary"):
        if texto_setlist:
            linhas_set = texto_setlist.split('\n')
            texto_final_insta = "🎵 HOJE NO SOM DA ILHA 🏝️\n\n"
            linhas_processadas = 0
            
            for linha in linhas_set:
                linha = linha.strip()
                if not linha:
                    continue
                
                # Limpezas básicas caso a linha venha com caminho ou .mp3
                if "\\" in linha:
                    linha = linha.split("\\")[-1]
                if linha.lower().endswith(".mp3"):
                    linha = linha[:-4]
                # Remove marcas de SC e compositores para a leitura do nome do artista ficar limpa
                linha_limpa = re.sub(r'\s*-\s*sc\s*$', '', linha, flags=re.IGNORECASE)
                linha_limpa = re.sub(r'\(comp\.[^)]+\)', '', linha_limpa, flags=re.IGNORECASE)
                
                partes = [p.strip() for p in linha_limpa.split(" - ")]
                
                if len(partes) >= 2:
                    artista_original = partes[0]
                    musica_original = partes[1]
                    
                    # Procura o @ do artista principal no banco de dados
                    artista_chave = artista_original.lower().strip()
                    artista_marcado = dicionario_artistas.get(artista_chave, artista_original)
                    
                    texto_final_insta += f"▪️ {artista_marcado} - {musica_original}\n"
                    linhas_processadas += 1
            
            if lines_processadas > 0:
                texto_final_insta += "\nSintonize em 100.1 FM ou no nosso site! 📻✨"
                
                st.success("✨ Texto gerado perfeitamente! Só copiar e postar:")
                st.text_area("Texto Pronto:", value=texto_final_insta, height=250)
                st.caption("Dica: Clique dentro da caixa acima, aperte Ctrl+A e depois Ctrl+C.")
            else:
                st.warning("Nenhuma música pôde ser formatada. Certifique-se de usar o padrão 'Artista - Música'.")
        else:
            st.warning("Cole a lista de músicas do setlist antes de gerar.")
