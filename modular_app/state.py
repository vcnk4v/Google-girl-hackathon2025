import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "patient_data" not in st.session_state:
        st.session_state.patient_data = {}
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    if "symptoms" not in st.session_state:
        st.session_state.symptoms = []
    if "lab_results" not in st.session_state:
        st.session_state.lab_results = {}
    if "diagnosis" not in st.session_state:
        st.session_state.diagnosis = None
    if "chief_complaint" not in st.session_state:
        st.session_state.chief_complaint = ""
    if "additional_symptoms" not in st.session_state:
        st.session_state.additional_symptoms = ""
    if "onset_info" not in st.session_state:
        st.session_state.onset_info = {}


def navigate_to(page):
    """Navigate to the specified page"""
    st.session_state.page = page


def reset_session_data():
    """Reset all patient-related session data"""
    st.session_state.patient_data = {}
    st.session_state.uploaded_image = None
    st.session_state.symptoms = []
    st.session_state.lab_results = {}
    st.session_state.diagnosis = None
    st.session_state.chief_complaint = ""
    st.session_state.additional_symptoms = ""
    st.session_state.onset_info = {}
