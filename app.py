!pip install streamlit plotly pandas pydeck pyngrok -q


import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

st.set_page_config(
    page_title="Observatório Territorial de Projetos",
    page_icon="🌎",
    layout="wide"
)

# ---------------------------------------------------
# CSS — MANTIDO COM SIDEBAR ESCURA
# ---------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #08120D 0%, #10261A 100%);
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #F5F5F5 !important;
}

section[data-testid="stSidebar"] {
    background-color: #071014 !important;
    border-right: 1px solid #1E2A2E;
}

section[data-testid="stSidebar"] * {
    color: #F5F5F5 !important;
}

div[data-baseweb="select"] {
    background-color: #11191D !important;
    border-radius: 10px !important;
    border: 1px solid #2B353A !important;
}

div[data-baseweb="select"] > div {
    background-color: #11191D !important;
    color: #F5F5F5 !important;
}

div[data-baseweb="popover"] {
    background-color: #11191D !important;
}

ul[role="listbox"] {
    background-color: #11191D !important;
}

li[role="option"] {
    background-color: #11191D !important;
    color: #F5F5F5 !important;
}

span[data-baseweb="tag"] {
    background-color: #2E7D32 !important;
    color: #FFFFFF !important;
}

.stRadio label {
    color: #F5F5F5 !important;
}

.stSlider label, .stSlider span, .stSlider div {
    color: #F5F5F5 !important;
}

[data-testid="stMetric"] {
    background-color: rgba(17,25,29,0.95);
    border: 1px solid #2B353A;
    border-radius: 16px;
    padding: 14px;
}

.block-container {
    padding-top: 1.5rem;
}

[data-testid="stDataFrame"] {
    background-color: #11191D;
    border-radius: 12px;
    border: 1px solid #2B353A;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

a {
    color: #81C784 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DADOS FICTÍCIOS
# ---------------------------------------------------

dados = pd.DataFrame({
    "Território": [
        "Alto Rio Negro", "Alto Rio Negro", "Alto Rio Negro",
        "Xingu", "Xingu", "Xingu",
        "Tapajós", "Tapajós", "Tapajós",
        "Yanomami", "Yanomami", "Yanomami",
        "Vale do Javari", "Vale do Javari", "Vale do Javari"
    ],
    "Categoria": [
        "Monitoramento territorial", "Bioeconomia", "Fortalecimento institucional",
        "Monitoramento territorial", "Proteção florestal", "Segurança alimentar",
        "Bioeconomia", "Proteção florestal", "Fortalecimento institucional",
        "Monitoramento territorial", "Saúde territorial", "Proteção florestal",
        "Proteção florestal", "Segurança alimentar", "Fortalecimento institucional"
    ],
    "Status": [
        "Em andamento", "Concluído", "Em planejamento",
        "Em andamento", "Em andamento", "Concluído",
        "Concluído", "Em andamento", "Em planejamento",
        "Em andamento", "Em planejamento", "Em andamento",
        "Em andamento", "Concluído", "Em planejamento"
    ],
    "Projetos": [5, 4, 3, 7, 6, 5, 4, 4, 2, 3, 2, 2, 4, 3, 2],
    "Famílias Beneficiadas": [1600, 1400, 1200, 2500, 2100, 1500, 1300, 1500, 700, 900, 600, 600, 1200, 900, 700],
    "Área Protegida (ha)": [620000, 510000, 370000, 950000, 870000, 580000, 370000, 410000, 200000, 510000, 320000, 370000, 700000, 620000, 430000],
    "Execução (%)": [72, 100, 25, 68, 54, 100, 100, 61, 30, 49, 22, 58, 63, 100, 34],
    "Ano": [2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024]
})

mapa = pd.DataFrame({
    "Território": ["Alto Rio Negro", "Xingu", "Tapajós", "Yanomami", "Vale do Javari"],
    "lat": [-0.1807, -11.1800, -3.4653, 2.8200, -4.5000],
    "lon": [-66.5000, -53.2000, -55.0000, -63.1300, -71.0000]
})

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("## Vivi Assessoria Antropológica")
st.sidebar.markdown("Protótipo conceitual para monitoramento territorial e visualização estratégica.")

territorio = st.sidebar.selectbox(
    "Território",
    ["Todos"] + sorted(dados["Território"].unique()),
    key="territorio_filtro"
)

categoria = st.sidebar.multiselect(
    "Categoria",
    sorted(dados["Categoria"].unique()),
    default=sorted(dados["Categoria"].unique()),
    key="categoria_filtro"
)

status = st.sidebar.multiselect(
    "Status",
    sorted(dados["Status"].unique()),
    default=sorted(dados["Status"].unique()),
    key="status_filtro"
)

ano = st.sidebar.slider(
    "Ano",
    int(dados["Ano"].min()),
    int(dados["Ano"].max()),
    (int(dados["Ano"].min()), int(dados["Ano"].max())),
    key="ano_filtro"
)

# ---------------------------------------------------
# APLICAÇÃO DOS FILTROS
# ---------------------------------------------------

df = dados.copy()

if territorio != "Todos":
    df = df[df["Território"] == territorio]

df = df[
    df["Categoria"].isin(categoria)
    & df["Status"].isin(status)
    & df["Ano"].between(ano[0], ano[1])
]

mapa_filtrado = mapa[mapa["Território"].isin(df["Território"].unique())]

# ---------------------------------------------------
# CABEÇALHO
# ---------------------------------------------------

st.title("Observatório Territorial de Projetos Socioambientais")
st.markdown("Dashboard demonstrativo para acompanhamento de projetos, territórios, indicadores e execução física.")
st.caption("Protótipo conceitual com dados fictícios para demonstração técnica.")

# ---------------------------------------------------
# KPIs DINÂMICOS
# ---------------------------------------------------

total_projetos = int(df["Projetos"].sum()) if not df.empty else 0
total_territorios = df["Território"].nunique() if not df.empty else 0
total_familias = int(df["Famílias Beneficiadas"].sum()) if not df.empty else 0
total_area = int(df["Área Protegida (ha)"].sum()) if not df.empty else 0
media_execucao = df["Execução (%)"].mean() if not df.empty else 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Projetos monitorados", total_projetos)
c2.metric("Territórios", total_territorios)
c3.metric("Famílias beneficiadas", f"{total_familias:,}".replace(",", "."))
c4.metric("Área protegida", f"{total_area/1000000:.2f} mi ha".replace(".", ","))
c5.metric("Execução média", f"{media_execucao:.1f}%".replace(".", ","))

# ---------------------------------------------------
# MAPA + LEITURA EXECUTIVA
# ---------------------------------------------------

col1, col2 = st.columns([1, 1.6])

with col1:
    st.subheader("Mapa territorial")

    if not mapa_filtrado.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=mapa_filtrado,
            get_position='[lon, lat]',
            get_radius=70000,
            get_fill_color='[67, 160, 71, 190]',
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=float(mapa_filtrado["lat"].mean()),
            longitude=float(mapa_filtrado["lon"].mean()),
            zoom=4 if territorio != "Todos" else 3
        )

        deck = pdk.Deck(
            map_style=None,
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{Território}"}
        )

        st.pydeck_chart(deck, use_container_width=True, height=300)
    else:
        st.warning("Nenhum território encontrado para os filtros selecionados.")

with col2:
    st.subheader("Leitura executiva")

    if not df.empty:
        territorio_txt = territorio if territorio != "Todos" else "os territórios selecionados"

        st.markdown(
            f"""
            Para **{territorio_txt}**, o painel apresenta **{total_projetos} projetos monitorados**,
            com **{total_familias:,} famílias beneficiadas** e aproximadamente
            **{total_area:,} hectares** abrangidos por ações socioambientais.
            """.replace(",", ".")
        )

        st.progress(min(int(media_execucao), 100) / 100)
        st.caption(f"Execução média dos projetos filtrados: {media_execucao:.1f}%".replace(".", ","))
    else:
        st.warning("Ajuste os filtros para visualizar a análise.")

# ---------------------------------------------------
# GRÁFICOS DINÂMICOS
# ---------------------------------------------------

g1, g2 = st.columns(2)

with g1:
    st.subheader("Projetos por categoria")

    if not df.empty:
        resumo_categoria = df.groupby("Categoria", as_index=False)["Projetos"].sum()

        fig1 = px.bar(
            resumo_categoria,
            x="Projetos",
            y="Categoria",
            orientation="h",
            text="Projetos",
            color="Categoria"
        )

        fig1.update_layout(
            plot_bgcolor="#11191D",
            paper_bgcolor="#11191D",
            font_color="#F5F5F5",
            showlegend=False,
            height=380
        )

        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

with g2:
    st.subheader("Distribuição por status")

    if not df.empty:
        resumo_status = df.groupby("Status", as_index=False)["Projetos"].sum()

        fig2 = px.pie(
            resumo_status,
            names="Status",
            values="Projetos",
            hole=0.45
        )

        fig2.update_layout(
            plot_bgcolor="#11191D",
            paper_bgcolor="#11191D",
            font_color="#F5F5F5",
            height=380
        )

        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

g3, g4 = st.columns(2)

with g3:
    st.subheader("Evolução dos projetos monitorados")

    if not df.empty:
        evolucao = df.groupby("Ano", as_index=False)["Projetos"].sum()

        fig3 = px.line(
            evolucao,
            x="Ano",
            y="Projetos",
            markers=True
        )

        fig3.update_layout(
            plot_bgcolor="#11191D",
            paper_bgcolor="#11191D",
            font_color="#F5F5F5",
            height=360
        )

        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

with g4:
    st.subheader("Execução média por território")

    if not df.empty:
        execucao = df.groupby("Território", as_index=False)["Execução (%)"].mean()

        fig4 = px.bar(
            execucao,
            x="Território",
            y="Execução (%)",
            text="Execução (%)"
        )

        fig4.update_traces(texttemplate="%{text:.1f}%", textposition="outside")

        fig4.update_layout(
            plot_bgcolor="#11191D",
            paper_bgcolor="#11191D",
            font_color="#F5F5F5",
            height=360,
            yaxis_range=[0, 110]
        )

        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

# ---------------------------------------------------
# TABELA
# ---------------------------------------------------

st.subheader("Base demonstrativa filtrada")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.markdown("""
---
### Finalidade do protótipo

Este painel demonstra uma solução possível para apoiar a organização, leitura e comunicação
de informações de projetos socioambientais, permitindo análise por território, categoria,
status, período, famílias beneficiadas, área protegida e execução física.

**Protótipo conceitual desenvolvido para demonstração técnica de monitoramento territorial e visualização estratégica de projetos socioambientais.**
""")

!streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &>/content/logs.txt &

from pyngrok import ngrok

ngrok.kill()
public_url = ngrok.connect(8501)
print(public_url)
