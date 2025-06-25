from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

# Caminho base do repositório
BASE_PATH = Path(__file__).parent
DATA_AIH_PATH = BASE_PATH / "dados_corrigidos.csv"
DATA_MUN_PATH = BASE_PATH / "municipios.csv"


def safe_read_csv(file_or_path, sep: str) -> pd.DataFrame:
    if hasattr(file_or_path, "read"):
        return pd.read_csv(file_or_path, sep=sep, low_memory=False)
    else:
        try:
            return pd.read_csv(file_or_path, sep=sep, low_memory=False)
        except FileNotFoundError:
            st.warning(f"Arquivo **{file_or_path.name}** não encontrado. Por favor, envie o arquivo abaixo.")
            uploaded = st.file_uploader(
                f"Upload de {file_or_path.name}", type=["csv"], key=str(file_or_path)
            )
            if uploaded is None:
                st.stop()
            return pd.read_csv(uploaded, sep=sep, low_memory=False)


@st.cache_data(show_spinner="↻ Processando dados...")
def pre_process(data: pd.DataFrame, municipios: pd.DataFrame) -> pd.DataFrame:
    # Conversão de data
    data["data_aih"] = pd.to_datetime(
        data["ano_aih"].astype(str)
        + "-"
        + data["mes_aih"].astype(str).str.zfill(2)
        + "-01",
        format="%Y-%m-%d",
    )

    # Criação de chave IBGE (6 dígitos)
    data["cod6"] = data["codigo_municipio"].astype(str).str[:6]
    municipios["cod6"] = municipios["codigo_ibge"].astype(str).str[:6]

    # Merge com municípios
    df = data.merge(municipios, on="cod6", how="left", validate="m:1")

    # Conversão de texto para categoria
    cat_cols = df.select_dtypes(include="object").columns
    df[cat_cols] = df[cat_cols].astype("category")

    # Normalização para os gráficos de bolhas
    df["vl_normalizado"] = df["vl_total"] / df["vl_total"].max() * 30_000
    df["qtd_normalizado"] = df["qtd_total"] / df["qtd_total"].max() * 30_000

    return df


def main() -> None:
    st.title("Análise AIH e Municípios")

    aih_exists = DATA_AIH_PATH.exists()
    mun_exists = DATA_MUN_PATH.exists()

    if aih_exists and mun_exists:
        aih_df = safe_read_csv(DATA_AIH_PATH, sep=";")
        mun_df = safe_read_csv(DATA_MUN_PATH, sep=",")
    else:
        st.info(
            "Arquivos CSV não encontrados no repositório. Por favor, envie os arquivos manualmente."
        )
        aih_df = None
        mun_df = None
        uploaded_aih = st.file_uploader(
            "Envie o arquivo dados_corrigidos.csv", type=["csv"], key="aih"
        )
        uploaded_mun = st.file_uploader(
            "Envie o arquivo municipios.csv", type=["csv"], key="mun"
        )
        if uploaded_aih is not None and uploaded_mun is not None:
            aih_df = safe_read_csv(uploaded_aih, sep=";")
            mun_df = safe_read_csv(uploaded_mun, sep=",")

    if aih_df is not None and mun_df is not None:
        processed_df = pre_process(aih_df, mun_df)
        st.success("Dados carregados e processados com sucesso!")
        st.write(processed_df.head())
    else:
        st.warning("Aguardando arquivos para iniciar o processamento.")

if __name__ == "__main__":
    main()

