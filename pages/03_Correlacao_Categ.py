import streamlit as st
import pandas as pd
import plotly.express as px
from itertools import combinations
from scipy.stats import chi2_contingency
import numpy as np
from utils import safe_read_csv, pre_process, DATA_AIH_PATH, DATA_MUN_PATH
from iesb_streamlit_style import inject_css, banner, configure_plotly

# Funções de auxílio
def cramers_v(confusion_matrix: pd.DataFrame) -> float:
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.values.sum()
    r, k = confusion_matrix.shape
    return np.sqrt(chi2 / (n * (min(k - 1, r - 1))))


def cramers_matrix(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
    for col1, col2 in combinations(cols, 2):
        conf = pd.crosstab(df[col1], df[col2])
        v = cramers_v(conf)
        matrix.loc[col1, col2] = v
        matrix.loc[col2, col1] = v
    np.fill_diagonal(matrix.values, 1.0)
    return matrix

# Configuração da página
st.set_page_config(page_title="Correlação Categórica", layout="wide")
inject_css()
banner("Correlação Categórica", "IESB • Ciência de Dados")
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
cat_cols = df.select_dtypes(include="category").columns.tolist()
sel_cols = st.sidebar.multiselect("Colunas categóricas", cat_cols, default=cat_cols[:3])

# -------------------- Cálculo e Exibição --------------------
if len(sel_cols) < 2:
    st.info("Selecione pelo menos duas variáveis para correlacionar.")
else:
    corr_df = cramers_matrix(df, sel_cols)
    fig = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Matriz de Correlação Categórica (Cramér's V)"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------- Navegação --------------------
st.markdown("---")
st.write("[🏠 Voltar ao Dashboard](../app.py)")
