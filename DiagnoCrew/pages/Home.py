import streamlit as st
from state import navigate_to, reset_session_data


def render_home_page():
    """Render the home page"""
    st.title("Welcome to the Medical Diagnostic Assistant")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
        This system helps healthcare professionals analyze medical images, patient data, 
        and symptoms to assist in diagnosing diseases accurately and efficiently.
        
        ### How to use this application:
        
        1. **Patient Information**: Enter basic patient demographic and medical history data
        2. **Upload Medical Images**: Upload X-rays, MRIs, or other medical imaging for analysis
        3. **Symptoms & Lab Results**: Record patient symptoms and laboratory test results
        4. **Diagnostic Results**: Review the AI-assisted diagnostic recommendations
        
        ⚠️ **Note**: This is a prototype using mock data for demonstration purposes only.
        Do not use for actual medical diagnosis.
        """
        )

        if st.button(
            "Start New Diagnostic Session", type="primary", use_container_width=True
        ):
            # Reset session data
            reset_session_data()
            navigate_to("Patient_Information")
