import streamlit as st
import plotly.express as px
import pandas as pd
from utils import safe_read_csv, pre_process, DATA_AIH_PATH, DATA_MUN_PATH

# Configuração da página
st.set_page_config(page_title="Correlação Categórica", layout="wide")

# Título e subtítulo
st.title("Correlação Categórica")
st.markdown("IESB • Ciência de Dados")

# Carregamento e pré-processamento
csv_aih = safe_read_csv(DATA_AIH_PATH, sep=";")
csv_mun = safe_read_csv(DATA_MUN_PATH, sep=",")

df = pre_process(csv_aih, csv_mun)

# Seleção de variáveis categóricas
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
variavel_x = st.selectbox("Variável X", cat_cols)
variavel_y = st.selectbox("Variável Y", cat_cols)

# Tabela de contingência e exibição
contingencia = pd.crosstab(df[variavel_x], df[variavel_y], normalize="index")
st.subheader("Tabela de Contingência Normalizada")
st.write(contingencia)

# Gráfico de heatmap
fig = px.imshow(
    contingencia,
    text_auto=True,
    aspect="auto",
    title=f"Correlação entre {variavel_x} e {variavel_y}"
)
st.plotly_chart(fig, use_container_width=True)
