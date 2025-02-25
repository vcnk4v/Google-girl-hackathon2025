# pages/symptoms.py - Symptoms and lab results page
import streamlit as st
from datetime import datetime
import time
from components.patient_info_display import display_patient_info
from components.navigation_buttons import render_navigation_buttons
from constants import COMMON_SYMPTOMS, LAB_TESTS
from utils.diagnostics import run_diagnostic_analysis
from state import navigate_to


def render_symptoms_page():
    """Render the symptoms and lab results page"""
    st.title("Symptoms & Lab Results")

    # Display patient info
    display_patient_info()

    tab1, tab2 = st.tabs(["Symptoms", "Laboratory Results"])

    with tab1:
        render_symptoms_tab()

    with tab2:
        render_lab_results_tab()

    # Navigation buttons with custom action for next button
    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back to Image Upload", use_container_width=True):
            navigate_to("Upload_Images")

    with col2:
        if st.button(
            "Run Diagnostic Analysis", type="primary", use_container_width=True
        ):
            with st.spinner("Running diagnostic analysis..."):
                # Run the diagnostic analysis
                run_diagnostic_analysis()
            navigate_to("Diagnostic_Results")


def render_symptoms_tab():
    """Render the symptoms tab content"""
    st.subheader("Chief Complaint")
    chief_complaint = st.text_area(
        "Patient's primary complaint",
        value=st.session_state.get("chief_complaint", ""),
        height=100,
    )

    st.subheader("Symptom Duration")
    col1, col2 = st.columns(2)
    with col1:
        onset_date = st.date_input("Onset Date", value=datetime.now())
    with col2:
        duration_unit = st.selectbox(
            "Duration Unit", ["Days", "Weeks", "Months", "Years"], index=0
        )
        duration_value = st.number_input("Duration", min_value=1, value=1)

    st.subheader("Symptoms")
    st.markdown("Select all symptoms that apply:")

    # Create columns for symptoms
    cols = st.columns(3)
    selected_symptoms = []

    for i, symptom in enumerate(COMMON_SYMPTOMS):
        col_idx = i % 3
        with cols[col_idx]:
            if st.checkbox(symptom, value=symptom in st.session_state.symptoms):
                selected_symptoms.append(symptom)

    # Additional symptoms
    st.subheader("Additional Symptoms")
    additional_symptoms = st.text_area(
        "Enter any additional symptoms not listed above",
        value=st.session_state.get("additional_symptoms", ""),
    )

    # Save symptoms
    if st.button("Save Symptoms", use_container_width=True):
        st.session_state.symptoms = selected_symptoms
        st.session_state.chief_complaint = chief_complaint
        st.session_state.additional_symptoms = additional_symptoms
        st.session_state.onset_info = {
            "date": str(onset_date),
            "duration": f"{duration_value} {duration_unit}",
        }
        st.success("Symptoms saved successfully!")


def render_lab_results_tab():
    """Render the lab results tab content"""
    st.subheader("Laboratory Test Results")

    # Create a tab for each category of lab tests
    lab_tabs = st.tabs(list(LAB_TESTS.keys()))

    lab_results = {}

    for i, category in enumerate(LAB_TESTS.keys()):
        with lab_tabs[i]:
            st.markdown(f"Enter {category} values:")

            # Create a form-like layout for each category
            cols = st.columns(2)
            category_results = {}

            for j, test in enumerate(LAB_TESTS[category]):
                col_idx = j % 2
                with cols[col_idx]:
                    saved_value = st.session_state.lab_results.get(category, {}).get(
                        test, ""
                    )
                    value = st.text_input(
                        f"{test}", value=saved_value, key=f"lab_{category}_{test}"
                    )
                    if value:
                        category_results[test] = value

            lab_results[category] = category_results

    # Save lab results
    if st.button("Save Lab Results", use_container_width=True):
        st.session_state.lab_results = lab_results
        st.success("Lab results saved successfully!")
