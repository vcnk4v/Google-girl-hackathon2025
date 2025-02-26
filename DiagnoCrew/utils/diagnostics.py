# utils/diagnostics.py - Diagnostic utilities
import streamlit as st
import time
from datetime import datetime
from medical_assistants.backend_services import DiagnosticService


def run_diagnostic_analysis():
    """
    Run diagnostic analysis on patient data
    """
    diagnostic_service = DiagnosticService()

    patient_data = st.session_state.patient_data
    uploaded_images = st.session_state.uploaded_images
    symptoms = st.session_state.symptoms
    lab_results = st.session_state.lab_results
    chief_complaint = st.session_state.get("chief_complaint", "")
    additional_symptoms = st.session_state.get("additional_symptoms", "")
    onset_info = st.session_state.get("onset_info", {})

    # Send data to backend service
    result = diagnostic_service.process_diagnostic_data(
        patient_data=patient_data,
        uploaded_images=uploaded_images,
        symptoms=symptoms,
        lab_results=lab_results,
        chief_complaint=chief_complaint,
        additional_symptoms=additional_symptoms,
        onset_info=onset_info,
    )

    # Store the case ID
    st.session_state.case_id = result["case_id"]

    # Run the diagnostic analysis
    diagnosis = diagnostic_service.run_diagnosis(
        case_id=result["case_id"], data_package=result["data_package"]
    )

    # Store the diagnosis in session state
    st.session_state.diagnosis = diagnosis

    # Log success message
    st.success(f"Analysis complete! Case ID: {result['case_id']}")

    return st.session_state.diagnosis
