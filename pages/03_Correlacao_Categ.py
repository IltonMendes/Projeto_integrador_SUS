"""Página: Correlação entre variáveis qualitativas"""
import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations
from scipy.stats import chi2_contingency
import plotly.express as px
from utils import load_data, pre_process
from iesb_streamlit_style import inject_css, banner, configure_plotly

# -------------------- Helpers --------------------

def cramers_v(x, y):
    conf = pd.crosstab(x, y)
    chi2 = chi2_contingency(conf)[0]
    n = conf.values.sum()
    r, k = conf.shape
    phi2 = chi2 / n
    phi2_corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    r_corr = r - ((r-1)**2)/(n-1)
    k_corr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2_corr / max(1e-9, min((k_corr-1), (r_corr-1))))

@st.cache_data(show_spinner="↻ Matriz de Cramér's V…")
def cramers_matrix(df_cat):
    cols = df_cat.columns
    v = np.eye(len(cols))
    for i, j in combinations(range(len(cols)), 2):
        v[i, j] = v[j, i] = cramers_v(df_cat.iloc[:, i], df_cat.iloc[:, j])
    return pd.DataFrame(v, index=cols, columns=cols)

# -------------------- Layout --------------------

st.set_page_config(page_title="Correlação categórica", layout="wide")
inject_css(); banner("Correlação qualitativa", "IESB • Ciência de Dados"); configure_plotly()

raw_aih, raw_mun = load_data()
df = pre_process(raw_aih, raw_mun)
cat_cols = df.select_dtypes(include=["category", "object"]).columns.tolist()

sel_cols = st.sidebar.multiselect("Variáveis categóricas", cat_cols, default=cat_cols[:min(4, len(cat_cols))])

if len(sel_cols) < 2:
    st.info("Selecione pelo menos duas variáveis para correlacionar.")
    st.stop()

corr_df = cramers_matrix(df[sel_cols])
fig = px.imshow(corr_df, text_auto=".2f", aspect="auto",
                color_continuous_scale=[[0, "#FFFFFF"], [1, "#E60000"]],
                title="Matriz de Cramér's V")
st.plotly_chart(fig, use_container_width=True)

# -------------------- Navegação --------------------
st.page_link("app.py", label="🏠 Dashboard")
st.page_link("pages/02_Estatisticas.py", label="📊 Estatísticas")
st.page_link("pages/03_Correlacao_Categ.py", label="🔗 Correlação categórica", disabled=True)
