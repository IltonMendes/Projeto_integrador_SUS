import streamlit as st
import plotly.express as px

# Paleta de cores
PRIMARY_RED = "#E60000"
LIGHT_GRAY  = "#F5F5F5"
WHITE       = "#FFFFFF"
BLACK       = "#000000"


def inject_css() -> None:
    """Injeta CSS global compatível com a identidade visual do IESB."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        /* ----- BASE LAYOUT -------------------------------------------------- */
        body {{
            background-color: {LIGHT_GRAY};
            font-family: 'Roboto', sans-serif;
        }}

        /* ----- BANNER -------------------------------------------------------- */
        .banner {{
            background-color: {PRIMARY_RED};
            padding: 1.2rem 1rem;
            border-radius: 0.4rem;
            margin-bottom: 1.5rem;
        }}
        .banner h1, .banner h2 {{
            color: {WHITE};
            text-align: center;
            margin: 0;
        }}
        .banner h1 {{ font-size: 2.2rem; }}
        .banner h2 {{ font-size: 1.1rem; font-weight: 300; }}

        /* ----- BOTÕES -------------------------------------------------------- */
        button {{
            background-color: {PRIMARY_RED};
            color: {WHITE};
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
        }}
        button:hover {{
            background-color: #bf0000;
            color: {WHITE};
        }}

        /* ----- SLIDER E SELECT ------------------------------------------------ */
        div[data-baseweb="select"] > div {{
            border: 1px solid {PRIMARY_RED};
        }}
        div[data-baseweb="slider"] [role="slider"] {{
            background-color: {PRIMARY_RED};
        }}

        /* ----- TABELAS -------------------------------------------------------- */
        thead tr th {{
            background-color: {PRIMARY_RED} !important;
            color: {WHITE} !important;
        }}
        tbody tr th {{
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
    """Renderiza um título com subtítulo (opcional) com identidade visual."""
    st.markdown(
        f"""
        <div class="banner">
            <h1>{title}</h1>
            {f'<h2>{subtitle}</h2>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def configure_plotly() -> None:
    """Define as cores padrão do Plotly para combinar com a paleta visual."""
    px.defaults.template = "plotly_white"
    px.defaults.color_discrete_sequence = [PRIMARY_RED, BLACK, "#7F7F7F"]


