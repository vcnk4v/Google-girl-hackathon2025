# components/patient_info_display.py - Component to display patient information
import streamlit as st


def display_patient_info():
    """Display basic patient information in a banner"""
    if st.session_state.patient_data:
        st.info(
            f"Patient: {st.session_state.patient_data.get('first_name', '')} "
            f"{st.session_state.patient_data.get('last_name', '')} | "
            f"ID: {st.session_state.patient_data.get('id', '')} | "
            f"Age: {st.session_state.patient_data.get('age', '')}"
        )
