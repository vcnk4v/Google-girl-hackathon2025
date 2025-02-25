# app.py - Main application file
import streamlit as st
from datetime import datetime
import time

# Import modules
from config import configure_page
from state import initialize_session_state
from pages.Home import render_home_page
from components.sidebar import render_sidebar
from pages.Patient_Information import render_patient_page
from pages.Upload_Images import render_images_page
from pages.Symptoms_Lab_Results import render_symptoms_page
from pages.Diagnostic_Results import render_results_page

# Configure the page
configure_page()

# Initialize session state
initialize_session_state()

# Render sidebar navigation
render_sidebar()

# Render the appropriate page based on session state
if st.session_state.page == "Home":
    render_home_page()
elif st.session_state.page == "Patient_Information":
    render_patient_page()
elif st.session_state.page == "Upload_Images":
    render_images_page()
elif st.session_state.page == "Symptoms_Lab_Results":
    render_symptoms_page()
elif st.session_state.page == "Diagnostic_Results":
    render_results_page()
