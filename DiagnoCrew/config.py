import streamlit as st


def configure_page():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="Medical Diagnostic Assistant",
        page_icon="🏥",
        layout="wide",
        # initial_sidebar_state="expanded",
    )
    hide_app_nav = """
    <style>
        [data-testid="stSidebarNav"] ul {
            padding-top: 0px;
        }
        [data-testid="stSidebarNav"] ul li {
            display: none;
        }
    </style>
    """
    st.markdown(hide_app_nav, unsafe_allow_html=True)
