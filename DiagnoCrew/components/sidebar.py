# components/sidebar.py - Sidebar navigation component
import streamlit as st
from state import navigate_to


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.title("DiagnoCrew")
        st.caption("AI-assisted diagnostic tool")

        st.subheader("Navigation")
        if st.button("Home", use_container_width=True):
            navigate_to("home")
        if st.button("Patient Information", use_container_width=True):
            navigate_to("patient")
        if st.button("Upload Medical Images", use_container_width=True):
            navigate_to("images")
        if st.button("Symptoms & Lab Results", use_container_width=True):
            navigate_to("symptoms")
        if st.button("Diagnostic Results", use_container_width=True):
            navigate_to("results")

        st.divider()
        st.caption("This is a prototype for demonstration purposes only.")
        st.caption("Built using Streamlit and Google AI Studio.")
