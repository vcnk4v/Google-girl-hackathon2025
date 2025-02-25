# pages/patient.py - Patient information page
import streamlit as st
import time
from datetime import datetime
from state import navigate_to
from constants import MEDICAL_CONDITIONS, BLOOD_TYPES


def render_patient_page():
    """Render the patient information page"""
    st.title("Patient Information")

    with st.form("patient_info_form"):
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)

        with col1:
            patient_id = st.text_input(
                "Patient ID", value=st.session_state.patient_data.get("id", "")
            )
            first_name = st.text_input(
                "First Name", value=st.session_state.patient_data.get("first_name", "")
            )
            last_name = st.text_input(
                "Last Name", value=st.session_state.patient_data.get("last_name", "")
            )

        with col2:
            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=st.session_state.patient_data.get("age", 30),
            )

            # Get gender index
            gender_options = ["Male", "Female", "Other"]
            gender_index = 0
            if "gender" in st.session_state.patient_data:
                try:
                    gender_index = gender_options.index(
                        st.session_state.patient_data["gender"]
                    )
                except ValueError:
                    gender_index = 0

            gender = st.selectbox("Gender", gender_options, index=gender_index)
            dob = st.date_input("Date of Birth", value=None)

        st.subheader("Medical History")
        col1, col2 = st.columns(2)

        with col1:
            height = st.number_input(
                "Height (cm)",
                min_value=0.0,
                value=st.session_state.patient_data.get("height", 170.0),
            )
            weight = st.number_input(
                "Weight (kg)",
                min_value=0.0,
                value=st.session_state.patient_data.get("weight", 70.0),
            )

            # Get blood type index
            blood_type_index = 8  # Default to "Unknown"
            if "blood_type" in st.session_state.patient_data:
                try:
                    blood_type_index = BLOOD_TYPES.index(
                        st.session_state.patient_data["blood_type"]
                    )
                except ValueError:
                    blood_type_index = 8

            blood_type = st.selectbox("Blood Type", BLOOD_TYPES, index=blood_type_index)

        with col2:
            allergies = st.text_area(
                "Allergies", value=st.session_state.patient_data.get("allergies", "")
            )
            medications = st.text_area(
                "Current Medications",
                value=st.session_state.patient_data.get("medications", ""),
            )

        existing_conditions = st.multiselect(
            "Existing Medical Conditions",
            MEDICAL_CONDITIONS,
            default=st.session_state.patient_data.get("existing_conditions", []),
        )

        family_history = st.text_area(
            "Family Medical History",
            value=st.session_state.patient_data.get("family_history", ""),
        )

        submitted = st.form_submit_button(
            "Save Patient Information", type="primary", use_container_width=True
        )

        if submitted:
            # Calculate BMI
            bmi = None
            if height > 0:
                bmi = round(weight / ((height / 100) ** 2), 1)

            # Save to session state
            st.session_state.patient_data = {
                "id": patient_id,
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
                "gender": gender,
                "dob": str(dob) if dob else None,
                "height": height,
                "weight": weight,
                "blood_type": blood_type,
                "allergies": allergies,
                "medications": medications,
                "existing_conditions": existing_conditions,
                "family_history": family_history,
                "bmi": bmi,
            }
            st.success("Patient information saved successfully!")
            navigate_to("Upload_Images")
