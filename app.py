from __future__ import annotations
from pathlib import Path
import plotly.express as px
import pydeck as pdk
import streamlit as st

from utils import load_data, pre_process

TITLE = "Relatório de Produção Hospitalar – SUS"
SUBTITLE = "IESB • Ciência de Dados"
LOGO_PATH = Path("images/logo.png").resolve()


# Sidebar – filtros 

def sidebar_filters(df):
    st.sidebar.header("🔎 Filtros")
    modo = st.sidebar.radio("Tipo de dado", ("Valor", "Quantidade"), horizontal=True)
    anos = sorted(df["data_aih"].dt.year.unique())
    anos_sel = st.sidebar.multiselect("Ano", anos, default=anos)
    return modo, anos_sel


# Métricas 

def metric(df):
    col1, col2 = st.columns(2)
    col1.metric("💰 Valor total gasto", f"R$ {df['vl_total'].sum():,.2f}")
    col2.metric("🏥 Procedimentos", f"{df['qtd_total'].sum():,}")


# Gráficos principais

def bar_charts(df, modo):
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


def time_series(df, modo):
    coluna = "vl_total" if modo == "Valor" else "qtd_total"
    df_mensal = df.groupby("data_aih")[coluna].sum().reset_index()
    fig = px.line(df_mensal, x="data_aih", y=coluna, markers=True,
                  labels={"data_aih": "Data", coluna: modo},
                  title=f"{modo} mensal")
    st.plotly_chart(fig, use_container_width=True)


def bubble_map(df, modo):
    valor, raio = ("vl_total", "vl_normalizado") if modo == "Valor" else ("qtd_total", "qtd_normalizado")
    df_map = df.dropna(subset=["latitude", "longitude", raio])
    if df_map.empty:
        st.info("Sem dados geográficos para o filtro atual.")
        return

    st.subheader(f"Distribuição geográfica por {modo.lower()}")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=df_map["latitude"].mean(),
                                         longitude=df_map["longitude"].mean(), zoom=5),
        layers=[pdk.Layer("ScatterplotLayer", data=df_map,
                          get_position="[longitude, latitude]", get_radius=raio,
                          get_fill_color="[230, 0, 0, 160]", pickable=True)],
        tooltip={"text": "{nome_municipio}\nValor: R$ {vl_total:,.2f}\nQtd: {qtd_total}"}
    ))


# Página principal

def main():
    st.set_page_config(page_title=TITLE, layout="wide")

    if LOGO_PATH.exists():
        st.sidebar.image(str(LOGO_PATH), width=140)

    raw_aih, raw_mun = load_data()
    df = pre_process(raw_aih, raw_mun)

    # Filtros 
    modo, anos = sidebar_filters(df)
    df_filtro = df[df["data_aih"].dt.year.isin(anos)]

    metric(df_filtro)
    col_left, col_right = st.columns((3, 2), gap="medium")
    with col_left:
        bar_charts(df_filtro, modo)
    with col_right:
        time_series(df_filtro, modo)

    st.divider(); bubble_map(df_filtro, modo)

    # Navegação
    st.page_link("app.py", label="🏠 Dashboard", disabled=True)
    st.page_link("pages/02_Estatisticas.py", label="📊 Estatísticas")
    st.page_link("pages/03_Correlacao.py", label="🔗 Correlação categórica")

if __name__ == "__main__":
    main()









