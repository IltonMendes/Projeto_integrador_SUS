############################################
# IESB Streamlit Style Helper
# ------------------------------------------
# Import this module in your Streamlit app
# and call:
#   inject_css()
#   banner("Your title", "optional subtitle")
#   configure_plotly()
# right after st.set_page_config(...)
############################################

import streamlit as st
import plotly.express as px

# Brand palette
PRIMARY_RED = "#E60000"
LIGHT_GRAY  = "#F5F5F5"
WHITE       = "#FFFFFF"
BLACK       = "#000000"


def inject_css() -> None:
    """Inject global CSS overrides that match IESB visual identity."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        /* ----- BASE LAYOUT -------------------------------------------------- */
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: {LIGHT_GRAY};
            font-family: 'Roboto', sans-serif;
        }}

        /* ----- TITLE BANNER ------------------------------------------------- */
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

        /* ----- SIDEBAR ------------------------------------------------------ */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {PRIMARY_RED};
        }}
        [data-testid="stSidebar"] *, .css-q8sbsg {{
            color: {WHITE} !important;
        }}

        /* ----- WIDGETS ------------------------------------------------------ */
        div.stButton > button {{
            background-color: {PRIMARY_RED};
            color: {WHITE};
            border: none;
            border-radius: 4px;
        }}
        div.stButton > button:hover {{
            background-color: #bf0000;
            color: {WHITE};
        }}
        /* selectbox & multiselect borders */
        div[data-baseweb="select"] > div {{
            border: 1px solid {PRIMARY_RED};
        }}
        /* slider track */
        div[data-baseweb="slider"] [role="slider"] {{
            background-color: {PRIMARY_RED};
        }}

        /* ----- TABLES ------------------------------------------------------- */
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
    """Render a branded title + subtitle block (optional)."""
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
    """Set Plotly defaults to align charts with IESB palette."""
    px.defaults.template = "plotly_white"
    px.defaults.color_discrete_sequence = [PRIMARY_RED, BLACK, "#7F7F7F"]


# ----------------------- HOW TO USE --------------------------------------- #
# import iesb_streamlit_style as style
# style.inject_css()
# style.banner("Relatório de Produção Hospitalar – SUS", "Centro Universitário IESB")
# style.configure_plotly()
# --------------------------------------------------------------------------

