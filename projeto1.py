import streamlit as st
import pandas as pd
import openpyxl
# Função para carregar o banco de ideias
def load_data(ideias):
    return pd.read_excel(ideias)
# Função para salvar atualizações no banco de ideias
def save_data(df, ideias):
    df.to_excel(ideias, index=False)
# Interface do Streamlit
st.title("Banco de Ideias Sustentáveis para Parques Urbanos")

# Carregando o arquivo Excel
uploaded_file = st.file_uploader("ideias", type="xlsx")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Exibir as primeiras linhas do banco de ideias
    st.write("Prévia do Banco de Ideias")
    st.dataframe(df.head())

    # Permitir edição dos dados
    st.write("Adicione uma nova ideia ao banco:")
    with st.form(key='new_idea_form'):
        ideia = st.text_input("Ideia")
        referencia_visual = st.text_input("Referência Visual")
        referencia_tecnica = st.text_input("Referência Técnica")
        referencia_legal = st.text_input("Referência Legal")
        aspectos_positivos = st.text_area("Aspectos Positivos")
        aspectos_negativos = st.text_area("Aspectos Negativos")
        comentario_geral = st.text_area("Comentário Geral")
        
        categoria_projeto = st.selectbox(
            "Categoria do Projeto", 
            ["Plano Clima", "Plano Bacia", "Pacto da Restauração da Mata Atlântica", "Plano de Desenvolvimento Rural Sustentável", "ODS", "Soluções Baseadas na Natureza"]
        )
        investimento_implantacao = st.number_input("Investimento de Implantação", min_value=0.0, format="%f")
        investimento_manutencao = st.number_input("Investimento de Manutenção", min_value=0.0, format="%f")
        
        submit_button = st.form_submit_button(label="Adicionar Ideia")
        
        # Se o botão for clicado, adicionar nova linha ao DataFrame
        if submit_button:
            new_row = {
                "Ideia": ideia,
                "Referência Visual": referencia_visual,
                "Referência Técnica": referencia_tecnica,
                "Referência Legal": referencia_legal,
                "Aspectos Positivos": aspectos_positivos,
                "Aspectos Negativos": aspectos_negativos,
                "Comentário Geral": comentario_geral,
                "Categoria do Projeto": categoria_projeto,
                "Investimento de Implantação": investimento_implantacao,
                "Investimento de Manutenção": investimento_manutencao
            }
            
            df = df.append(new_row, ignore_index=True)
            st.success("Ideia adicionada com sucesso!")
# Mostrar banco de ideias atualizado
    st.write("Banco de Ideias Atualizado")
    st.dataframe(df)
    
    # Permitir download do arquivo atualizado
    if st.button("Baixar Banco de Ideias Atualizado"):
        save_data(df, "ideias_atualizadas.xlsx")
        with open("ideias_atualizadas.xlsx", "rb") as f:
            st.download_button(label="Download", data=f, file_name="ideias_atualizadas.xlsx")
