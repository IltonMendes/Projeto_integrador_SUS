import streamlit as st
import plotly.express as px
from utils import safe_read_csv, pre_process, DATA_AIH_PATH, DATA_MUN_PATH

# Configuração da página
st.set_page_config(page_title="Estatísticas Descritivas", layout="wide")

# Título e subtítulo
st.title("Estatísticas Descritivas")
st.markdown("IESB • Ciência de Dados")

# Carregamento e pré-processamento
csv_aih = safe_read_csv(DATA_AIH_PATH)
csv_mun = safe_read_csv(DATA_MUN_PATH)
df = pre_process(csv_aih, csv_mun)

# Seleção de variáveis numéricas
colunas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
selecionada = st.selectbox("Selecione a variável", colunas)

# Exibição de estatísticas
st.subheader(f"Estatísticas da variável {selecionada}")
descr = df[selecionada].describe()
st.write(descr)

# Gráfico de distribuição
fig = px.histogram(df, x=selecionada, nbins=50, title=f"Distribuição de {selecionada}")
st.plotly_chart(fig, use_container_width=True)

# -------------------- Navegação --------------------
st.markdown("---")
st.write("[🏠 Voltar ao Dashboard](../app.py)")

