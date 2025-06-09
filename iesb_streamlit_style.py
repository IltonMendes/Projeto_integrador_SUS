import streamlit as st
import plotly.express as px

# Cores institucionais
PRIMARY_RED = "#E60000"
LIGHT_GRAY = "#F5F5F5"
WHITE = "#FFFFFF"
BLACK = "#000000"

def inject_css() -> None:
    """Aplica CSS personalizado para identidade visual do IESB."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        body, html {{
            font-family: 'Roboto', sans-serif;
            background-color: {LIGHT_GRAY};
        }}

        /* Banner */
        .iesb-banner {{
            background-color: {PRIMARY_RED};
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        .iesb-banner h1 {{
            color: {WHITE};
            font-size: 2rem;
            text-align: center;
            margin: 0;
        }}
        .iesb-banner h2 {{
            color: {WHITE};
            font-size: 1.2rem;
            font-weight: 300;
            text-align: center;
            margin-top: 0.5rem;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {PRIMARY_RED};
        }}
        [data-testid="stSidebar"] *, .css-q8sbsg {{
            color: {WHITE} !important;
        }}

        /* Botões */
        div.stButton > button {{
            background-color: {PRIMARY_RED};
            color: {WHITE};
            border: none;
            border-radius: 4px;
        }}
        div.stButton > button:hover {{
            background-color: #bf0000;
        }}

        /* Select e Slider */
        div[data-baseweb="select"] > div {{
            border: 1px solid {PRIMARY_RED};
        }}
        div[data-baseweb="slider"] [role="slider"] {{
            background-color: {PRIMARY_RED};
        }}

        /* Tabela */
        thead tr th {{
            background-color: {PRIMARY_RED} !important;
            color: {WHITE} !important;
        }}
        tbody tr td {{
            color: {BLACK};
        }}
        .dataframe {{
            border-radius: 6px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def banner(title: str, subtitle: str = "") -> None:
    """Exibe um banner com título e subtítulo."""
    st.markdown(
        f"""
        <div class="iesb-banner">
            <h1>{title}</h1>
            {f"<h2>{subtitle}</h2>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

def configure_plotly() -> None:
    """Aplica a paleta de cores do IESB aos gráficos Plotly."""
    px.defaults.template = "plotly_white"
    px.defaults.color_discrete_sequence = [PRIMARY_RED, BLACK, "#7F7F7F"]

