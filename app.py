import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt

st.set_page_config(
    page_title="Observatório Territorial de Projetos",
    page_icon="🌎",
    layout="wide"
)

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

df = dados.copy()

if territorio != "Todos":
    df = df[df["Território"] == territorio]

df = df[
    df["Categoria"].isin(categoria)
    & df["Status"].isin(status)
    & df["Ano"].between(ano[0], ano[1])
]

mapa_filtrado = mapa[mapa["Território"].isin(df["Território"].unique())]

st.title("Observatório Territorial de Projetos Socioambientais")
st.markdown("Dashboard demonstrativo para acompanhamento de projetos, territórios, indicadores e execução física.")
st.caption("Protótipo conceitual com dados fictícios para demonstração técnica.")

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

col1, col2 = st.columns([1, 1.6])

with col1:
    st.subheader("Mapa territorial")

    if not mapa_filtrado.empty:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=mapa_filtrado,
            get_position='[lon, lat]',
            get_radius=70000,
            get_fill_color='[124, 179, 66, 190]',
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
            <div class="card-text">
            Para <b>{territorio_txt}</b>, o painel apresenta <b>{total_projetos} projetos monitorados</b>,
            com <b>{total_familias:,} famílias beneficiadas</b> e aproximadamente
            <b>{total_area:,} hectares</b> abrangidos por ações socioambientais.
            <br><br>
            A execução média dos projetos filtrados é de <b>{media_execucao:.1f}%</b>.
            </div>
            """.replace(",", "."),
            unsafe_allow_html=True
        )

        st.progress(min(int(media_execucao), 100) / 100)
    else:
        st.warning("Ajuste os filtros para visualizar a análise.")

def chart_base():
    return (
        alt.Chart()
        .properties(height=340)
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor="#C8D6C9",
            titleColor="#C8D6C9",
            gridColor="#26352C"
        )
        .configure_title(
            color="#F5F5F5",
            fontSize=15,
            anchor="start"
        )
        .configure_legend(
            labelColor="#F5F5F5",
            titleColor="#F5F5F5"
        )
    )

g1, g2 = st.columns(2)

with g1:
    st.subheader("Projetos por categoria")

    if not df.empty:
        resumo_categoria = (
            df.groupby("Categoria", as_index=False)["Projetos"]
            .sum()
            .sort_values("Projetos", ascending=True)
        )

        chart = (
            alt.Chart(resumo_categoria)
            .mark_bar(cornerRadiusEnd=5)
            .encode(
                x=alt.X("Projetos:Q", title="Projetos"),
                y=alt.Y("Categoria:N", sort="-x", title=""),
                color=alt.Color(
                    "Categoria:N",
                    legend=None,
                    scale=alt.Scale(range=["#7CB342", "#43A047", "#26A69A", "#A5D6A7", "#FFB74D"])
                ),
                tooltip=["Categoria", "Projetos"]
            )
            .properties(height=360)
            .configure_view(strokeWidth=0)
            .configure_axis(labelColor="#C8D6C9", titleColor="#C8D6C9", gridColor="#26352C")
            .configure(background="#11191D")
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

with g2:
    st.subheader("Projetos por status")

    if not df.empty:
        resumo_status = df.groupby("Status", as_index=False)["Projetos"].sum()

        chart = (
            alt.Chart(resumo_status)
            .mark_arc(innerRadius=65, outerRadius=130)
            .encode(
                theta=alt.Theta("Projetos:Q"),
                color=alt.Color(
                    "Status:N",
                    scale=alt.Scale(
                        domain=["Concluído", "Em andamento", "Em planejamento"],
                        range=["#7CB342", "#1E88E5", "#FFB74D"]
                    ),
                    legend=alt.Legend(orient="bottom")
                ),
                tooltip=["Status", "Projetos"]
            )
            .properties(height=360)
            .configure_view(strokeWidth=0)
            .configure_legend(labelColor="#F5F5F5", titleColor="#F5F5F5")
            .configure(background="#11191D")
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

g3, g4 = st.columns(2)

with g3:
    st.subheader("Evolução dos projetos monitorados")

    if not df.empty:
        evolucao = df.groupby("Ano", as_index=False)["Projetos"].sum()

        line = (
            alt.Chart(evolucao)
            .mark_line(point=True, strokeWidth=3, color="#81C784")
            .encode(
                x=alt.X("Ano:O", title="Ano"),
                y=alt.Y("Projetos:Q", title="Projetos"),
                tooltip=["Ano", "Projetos"]
            )
            .properties(height=340)
            .configure_view(strokeWidth=0)
            .configure_axis(labelColor="#C8D6C9", titleColor="#C8D6C9", gridColor="#26352C")
            .configure(background="#11191D")
        )

        st.altair_chart(line, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

with g4:
    st.subheader("Execução média por território")

    if not df.empty:
        execucao = df.groupby("Território", as_index=False)["Execução (%)"].mean()

        bars = (
            alt.Chart(execucao)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
            .encode(
                x=alt.X("Território:N", title=""),
                y=alt.Y("Execução (%):Q", title="Execução (%)", scale=alt.Scale(domain=[0, 100])),
                color=alt.value("#1E88E5"),
                tooltip=["Território", alt.Tooltip("Execução (%):Q", format=".1f")]
            )
            .properties(height=340)
            .configure_view(strokeWidth=0)
            .configure_axis(labelColor="#C8D6C9", titleColor="#C8D6C9", gridColor="#26352C")
            .configure(background="#11191D")
        )

        st.altair_chart(bars, use_container_width=True)
    else:
        st.info("Sem dados para o filtro selecionado.")

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
