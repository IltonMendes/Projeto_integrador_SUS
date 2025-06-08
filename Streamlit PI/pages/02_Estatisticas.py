"""Página: Estatísticas Descritivas"""
import streamlit as st
import plotly.express as px
from utils import load_data, pre_process
from iesb_streamlit_style import inject_css, banner, configure_plotly

st.set_page_config(page_title="Estatísticas descritivas", layout="wide")
inject_css(); banner("Estatísticas descritivas", "IESB • Ciência de Dados"); configure_plotly()

raw_aih, raw_mun = load_data()
df = pre_process(raw_aih, raw_mun)

# -------------------- Sidebar --------------------
num_cols = df.select_dtypes(include="number").columns.tolist()
sel_cols = st.sidebar.multiselect("Variáveis numéricas", num_cols, default=[])

if not sel_cols:
    st.info("Selecione ao menos uma coluna na barra lateral.")
    st.stop()

# -------------------- Resumo --------------------
with st.expander("📋 Resumo estatístico"):
    if not sel_cols:
        st.write("Exibindo resumo estatístico de **todas as variáveis numéricas**.")
        st.dataframe(df[num_cols].describe().T)
    else:
        st.write(f"Exibindo resumo estatístico de: {', '.join(sel_cols)}")
        st.dataframe(df[sel_cols].describe().T)

# -------------------- Boxplots --------------------
if sel_cols:
    for col in sel_cols:
        fig = px.box(df, y=col, points="outliers", title=f"Boxplot · {col}")
        st.plotly_chart(fig, use_container_width=True)

# -------------------- Navegação --------------------
st.page_link("app.py", label="🏠 Visão geral")
st.page_link("pages/02_Estatisticas.py", label="📊 Estatísticas", disabled=True)
st.page_link("pages/03_Correlacao_Categ.py", label="🔗 Correlação categórica")
