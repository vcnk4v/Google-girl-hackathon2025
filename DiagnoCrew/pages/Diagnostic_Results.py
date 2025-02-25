# pages/results.py - Diagnostic results page
import streamlit as st
from PIL import Image
import io
from components.patient_info_display import display_patient_info
from state import navigate_to, reset_session_data


def render_results_page():
    """Render the diagnostic results page"""
    st.title("Diagnostic Results")

    # Display patient info
    display_patient_info()

    if not st.session_state.diagnosis:
        st.warning(
            "No diagnostic results available. Please complete the diagnostic analysis first."
        )
        if st.button("Go to Symptoms & Lab Results", use_container_width=True):
            navigate_to("Symptoms_Lab_Results")
    else:
        # Display diagnostic results
        diagnosis = st.session_state.diagnosis

        col1, col2 = st.columns([2, 1])

        with col1:
            display_primary_diagnosis(diagnosis)
            display_supporting_evidence(diagnosis)
            display_recommended_actions(diagnosis)
            display_differential_diagnoses(diagnosis)

        with col2:
            display_image_analysis()
            display_patient_symptoms()

        display_analysis_notes()
        display_action_buttons()


def display_primary_diagnosis(diagnosis):
    """Display the primary diagnosis section"""
    st.subheader("Primary Diagnosis")
    st.markdown(f"### {diagnosis['primary_diagnosis']}")
    st.progress(diagnosis["confidence"])
    st.caption(f"Confidence: {diagnosis['confidence'] * 100:.1f}%")


def display_supporting_evidence(diagnosis):
    """Display supporting evidence section"""
    st.subheader("Supporting Evidence")
    for evidence in diagnosis["supporting_evidence"]:
        st.markdown(f"- {evidence}")


def display_recommended_actions(diagnosis):
    """Display recommended actions section"""
    st.subheader("Recommended Actions")
    for action in diagnosis["recommended_actions"]:
        st.markdown(f"- {action}")
    st.divider()


def display_differential_diagnoses(diagnosis):
    """Display differential diagnoses section"""
    st.subheader("Differential Diagnoses")
    for diff in diagnosis["differential_diagnoses"]:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{diff['condition']}**")
            st.progress(diff["probability"])
        with col2:
            st.markdown(f"**{diff['probability'] * 100:.1f}%**")


def display_image_analysis():
    """Display image analysis section"""
    st.subheader("Image Analysis")
    if st.session_state.uploaded_image:
        image_data = st.session_state.uploaded_image["file"]
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption="Analyzed Image", use_container_width=True)

        st.markdown("**Key Findings**")
        st.markdown("- Finding 1: Sample observation")
        st.markdown("- Finding 2: Sample observation")
    else:
        st.write("No image available")


def display_patient_symptoms():
    """Display patient symptoms section"""
    st.subheader("Patient Symptoms")
    if st.session_state.symptoms:
        for symptom in st.session_state.symptoms:
            st.markdown(f"- {symptom}")
    else:
        st.write("No symptoms recorded")


def display_analysis_notes():
    """Display analysis notes section"""
    st.subheader("Analysis Notes")
    st.text_area("Add notes about this diagnosis", height=100, key="diagnosis_notes")


def display_action_buttons():
    """Display action buttons for the results page"""
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export Report (PDF)", use_container_width=True):
            st.info(
                "Exporting report... (This is a placeholder - actual PDF export would be implemented here)"
            )
    with col2:
        if st.button("Save to Patient Record", use_container_width=True):
            st.success("Diagnosis saved to patient record")
    with col3:
        if st.button("Start New Session", use_container_width=True):
            # Reset session data
            reset_session_data()
            navigate_to("Home")
