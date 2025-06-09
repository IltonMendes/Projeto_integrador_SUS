import streamlit as st
import plotly.express as px
from utils import safe_read_csv, pre_process, DATA_AIH_PATH, DATA_MUN_PATH
from iesb_streamlit_style import inject_css, banner, configure_plotly

# Configuração da página
st.set_page_config(page_title="Estatísticas Descritivas", layout="wide")
inject_css()
banner("Estatísticas Descritivas", "IESB • Ciência de Dados")
configure_plotly()

# Carregamento e pré-processamento dos dados
aio_df = safe_read_csv(DATA_AIH_PATH, sep=";")
mun_df = safe_read_csv(DATA_MUN_PATH, sep=",")
if aih_df is None or mun_df is None:
    st.warning("Aguardando arquivos para iniciar o processamento.")
    st.stop()

df = pre_process(aih_df, mun_df)

# -------------------- Sidebar --------------------
st.sidebar.header("Seleção de colunas")
num_cols = df.select_dtypes(include="number").columns.tolist()
sel_cols = st.sidebar.multiselect("Colunas numéricas", num_cols, default=num_cols[:3])

# -------------------- Resumo Estatístico --------------------
with st.expander("📋 Resumo Estatístico"):
    st.write(f"Exibindo resumo estatístico de: {', '.join(sel_cols)}")
    st.dataframe(df[sel_cols].describe().T)

# -------------------- Boxplots --------------------
for col in sel_cols:
    fig = px.box(df, y=col, points="outliers", title=f"Boxplot · {col}")
    st.plotly_chart(fig, use_container_width=True)

# -------------------- Navegação --------------------
st.markdown("---")
st.write("[🏠 Voltar ao Dashboard](../app.py)")

