from __future__ import annotations
from pathlib import Path
import plotly.express as px
import pydeck as pdk
import streamlit as st
import pandas as pd

from utils import safe_read_csv, pre_process

TITLE = "Relatório de Produção Hospitalar – SUS"
SUBTITLE = "IESB • Ciência de Dados"
# Ajuste no caminho relativo ao arquivo
LOGO_PATH = Path(__file__).parent / "images" / "logo.png"

# Definição dos caminhos de dados considerando o diretório do script
DATA_AIH_PATH = Path(__file__).parent / "dados_corrigidos.csv"
DATA_MUN_PATH = Path(__file__).parent / "municipios.csv"

# Sidebar – filtros
def sidebar_filters(df: pd.DataFrame) -> tuple[str, list[int]]:
    st.sidebar.header("🔎 Filtros")
    modo = st.sidebar.radio("Tipo de dado", ("Valor", "Quantidade"), horizontal=True)
    anos = sorted(df["data_aih"].dt.year.unique())
    anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)
    return modo, anos_sel

# Métricas
def metric(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)
    col1.metric("💰 Valor total gasto", f"R$ {df['vl_total'].sum():,.2f}")
    col2.metric("🏥 Procedimentos", f"{df['qtd_total'].sum():,}")

# Gráficos principais
def bar_charts(df: pd.DataFrame, modo: str) -> None:
    cols_valor = [f"vl_{i:02d}" for i in range(2, 9)]
    cols_qtd = [f"qtd_{i:02d}" for i in range(1, 9)]
    if modo == "Valor":
        serie = df[cols_valor].sum().sort_values(ascending=False)
        ytitle, title = "Valor (R$)", "Valor total por procedimento"
    else:
        serie = df[cols_qtd].sum().sort_values(ascending=False)
        ytitle, title = "Quantidade", "Quantidade total por procedimento"
    fig = px.bar(serie, labels={"index": "Procedimento", "value": ytitle}, text_auto=".2s", title=title)
    st.plotly_chart(fig, use_container_width=True)


def time_series(df: pd.DataFrame, modo: str) -> None:
    coluna = "vl_total" if modo == "Valor" else "qtd_total"
    df_mensal = df.groupby("data_aih")[coluna].sum().reset_index()
    fig = px.line(
        df_mensal,
        x="data_aih",
        y=coluna,
        markers=True,
        labels={"data_aih": "Data", coluna: modo},
        title=f"{modo} mensal"
    )
    st.plotly_chart(fig, use_container_width=True)


def bubble_map(df: pd.DataFrame, modo: str) -> None:
    valor, raio = ("vl_total", "vl_normalizado") if modo == "Valor" else ("qtd_total", "qtd_normalizado")
    df_map = df.dropna(subset=["latitude", "longitude", raio])
    if df_map.empty:
        st.info("Sem dados geográficos para o filtro atual.")
        return
    st.subheader(f"Distribuição geográfica por {modo.lower()}")
    st.pydeck_chart(
        pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=df_map["latitude"].mean(),
                longitude=df_map["longitude"].mean(),
                zoom=5
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_map,
                    get_position="[longitude, latitude]",
                    get_radius=raio,
                    get_fill_color="[230, 0, 0, 160]",
                    pickable=True
                )
            ],
            tooltip={"text": "{nome_municipio}\nValor: R$ {vl_total:,.2f}\nQtd: {qtd_total}"}
        )
    )


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    # Tenta ler dados locais; se não existir, solicita upload
    try:
        aih = safe_read_csv(DATA_AIH_PATH, sep=";")
    except FileNotFoundError:
        st.warning(f"Arquivo {DATA_AIH_PATH.name} não encontrado. Faça upload do arquivo.")
        uploaded = st.file_uploader(
            f"Upload de {DATA_AIH_PATH.name}", type=["csv"], key="upload_aih"
        )
        if not uploaded:
            st.stop()
        aih = pd.read_csv(uploaded, sep=";", low_memory=False)

    try:
        mun = safe_read_csv(DATA_MUN_PATH, sep=",")
    except FileNotFoundError:
        st.warning(f"Arquivo {DATA_MUN_PATH.name} não encontrado. Faça upload do arquivo.")
        uploaded = st.file_uploader(
            f"Upload de {DATA_MUN_PATH.name}", type=["csv"], key="upload_mun"
        )
        if not uploaded:
            st.stop()
        mun = pd.read_csv(uploaded, sep=",", low_memory=False)

    return aih, mun

@st.cache_data(show_spinner="↻ Lendo dados...")
def cached_load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    return load_data()


def main() -> None:
    st.set_page_config(page_title=TITLE, layout="wide")

    # Exibe logo se existir
    if LOGO_PATH.exists():
        st.sidebar.image(str(LOGO_PATH), width=140)

    raw_aih, raw_mun = cached_load_data()
    df = pre_process(raw_aih, raw_mun)

    modo, anos = sidebar_filters(df)
    df_filtro = df[df["data_aih"].dt.year.isin(anos)]

    metric(df_filtro)
    col_left, col_right = st.columns((3, 2), gap="medium")
    with col_left:
        bar_charts(df_filtro, modo)
    with col_right:
        time_series(df_filtro, modo)

    st.divider()
    bubble_map(df_filtro, modo)

    # Navegação entre páginas
    st.page_link("app.py", label="🏠 Dashboard", disabled=True)
    st.page_link("pages/02_Estatisticas.py", label="📊 Estatísticas")  
    st.page_link("pages/03_Correlacao.py", label="🔗 Correlação categórica")  

if __name__ == "__main__":
    main()







