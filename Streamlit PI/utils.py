from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_AIH_PATH = Path(r"C:\Users\Usuário\Desktop\Streamlit PI\dados_corrigidos.csv")
DATA_MUN_PATH = Path(r"C:\Users\Usuário\Desktop\Streamlit PI\municipios.csv")

# ------------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------------

def _safe_read_csv(path: Path, sep: str) -> pd.DataFrame:
    """Lê CSV local ou via upload quando ausente."""
    try:
        return pd.read_csv(path, sep=sep, low_memory=False)
    except FileNotFoundError:
        st.warning(f"Arquivo **{path.name}** não encontrado. Envie o CSV.")
        uploaded = st.file_uploader(f"Upload de {path.name}", type=["csv"], key=str(path))
        if uploaded is None:
            st.stop()
        return pd.read_csv(uploaded, sep=sep, low_memory=False)

# ------------------------------------------------------------------
# Pipeline de dados (cacheado)
# ------------------------------------------------------------------

@st.cache_data(show_spinner="↻ Lendo dados...")
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lê AIH + Municípios."""
    aih = _safe_read_csv(DATA_AIH_PATH, sep=";")
    mun = _safe_read_csv(DATA_MUN_PATH, sep=",")
    return aih, mun

@st.cache_data(show_spinner="↻ Processando dados...")
def pre_process(data: pd.DataFrame, municipios: pd.DataFrame) -> pd.DataFrame:
    """Merge, limpeza e colunas auxiliares."""
    # Data YYYY‑MM‑01
    data["data_aih"] = pd.to_datetime(
        data["ano_aih"].astype(str) + "-" + data["mes_aih"].astype(str).str.zfill(2) + "-01",
        format="%Y-%m-%d"
    )

    # Chave IBGE (6 dígitos)
    data["cod6"] = data["codigo_municipio"].astype(str).str[:6]
    municipios["cod6"] = municipios["codigo_ibge"].astype(str).str[:6]

    df = data.merge(municipios, on="cod6", how="left", validate="m:1")

    # Conversão de colunas de texto p/ category
    cat_cols = df.select_dtypes(include="object").columns
    df[cat_cols] = df[cat_cols].astype("category")

    # Tamanho p/ bolhas
    df["vl_normalizado"] = df["vl_total"] / df["vl_total"].max() * 30_000
    df["qtd_normalizado"] = df["qtd_total"] / df["qtd_total"].max() * 30_000

    return df
