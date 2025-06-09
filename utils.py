from __future__ import annotations
from pathlib import Path
import pandas as pd

def safe_read_csv(file_or_path, sep: str) -> pd.DataFrame:
    """
    Lê CSV a partir de um Path ou arquivo uploadado (UploadedFile).
    Não faz upload nem interação com Streamlit.
    """
    if hasattr(file_or_path, "read"):
        # É arquivo uploadado
        return pd.read_csv(file_or_path, sep=sep, low_memory=False)
    else:
        # É Path, tenta ler do disco
        if not Path(file_or_path).exists():
            raise FileNotFoundError(f"Arquivo {file_or_path} não encontrado.")
        return pd.read_csv(file_or_path, sep=sep, low_memory=False)


def pre_process(data: pd.DataFrame, municipios: pd.DataFrame) -> pd.DataFrame:
    data["data_aih"] = pd.to_datetime(
        data["ano_aih"].astype(str) + "-" + data["mes_aih"].astype(str).str.zfill(2) + "-01",
        format="%Y-%m-%d"
    )

    data["cod6"] = data["codigo_municipio"].astype(str).str[:6]
    municipios["cod6"] = municipios["codigo_ibge"].astype(str).str[:6]

    df = data.merge(municipios, on="cod6", how="left", validate="m:1")

    cat_cols = df.select_dtypes(include="object").columns
    df[cat_cols] = df[cat_cols].astype("category")

    df["vl_normalizado"] = df["vl_total"] / df["vl_total"].max() * 30_000
    df["qtd_normalizado"] = df["qtd_total"] / df["qtd_total"].max() * 30_000

    return df


