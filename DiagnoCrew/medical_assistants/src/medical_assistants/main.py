#!/usr/bin/env python
import sys
import warnings
import os
import json
from datetime import datetime
import re
import PIL.Image
import base64
from medical_assistants.crew import MedicalAssistants

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def process_output(output):
    """
    Process the crew output to ensure it's in the correct format.
    Removes markdown code blocks and extracts valid JSON.

    Args:
        output (str): The output from the crew

    Returns:
        dict: The processed diagnostic report
    """

    match = re.search(r"```json\s*({.*?})\s*```", output, re.DOTALL)
    if not match:
        raise ValueError("No JSON content found in the Markdown block.")

    json_string = match.group(1)  # Extract the JSON content

    # Step 2: Parse the JSON string into a Python dictionary
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON string: {str(e)}", e.doc, e.pos)


def run():
    """
    Run the medical diagnostic crew with patient information.

    Args:
        patient_data (dict): Patient demographic and medical history
        symptoms (dict): Patient symptoms and complaints
        lab_results (dict): Laboratory test results

    Returns:
        dict: The diagnostic report
    """
    patient_data = {
        "age": 45,
        "gender": "male",
        "medical_history": ["hypertension", "type 2 diabetes"],
        "medications": ["metformin", "lisinopril"],
    }

    symptoms = {
        "chief_complaint": "chest pain",
        "symptom_list": ["shortness of breath", "fatigue", "dizziness"],
        "onset_info": {"duration": "3 days", "severity": "moderate"},
    }

    lab_results = {
        "blood_pressure": "150/95",
        "heart_rate": 95,
        "blood_glucose": 180,
        "troponin": "elevated",
        "ekg": "abnormal",
    }
    image_results = {
        "findings": "The image shows very slight mass in the right lung.",
    }
    inputs = {
        "patient_data": json.dumps(patient_data),
        "symptoms": json.dumps(symptoms),
        "lab_results": json.dumps(lab_results),
        "image_results": json.dumps(image_results),
    }

    try:
        result = (MedicalAssistants().crew().kickoff(inputs=inputs)).raw
        result_processed = process_output(result)

        # Parse the report from the result
        try:
            return json.loads(result_processed)
        except:
            # If the result isn't valid JSON, return it as is
            return {"error": "Could not parse result as JSON", "raw_result": result}
    except Exception as e:
        return {"error": f"An error occurred while running the crew: {str(e)}"}


def train():
    """
    Train the crew for a given number of iterations.
    """

    sample_inputs = {
        "patient_data": json.dumps(
            {
                "age": 45,
                "gender": "male",
                "medical_history": ["hypertension", "type 2 diabetes"],
                "medications": ["metformin", "lisinopril"],
            }
        ),
        "symptoms": json.dumps(
            {
                "chief_complaint": "chest pain",
                "symptom_list": ["shortness of breath", "fatigue", "dizziness"],
                "onset_info": {"duration": "3 days", "severity": "moderate"},
            }
        ),
        "lab_results": json.dumps(
            {
                "blood_pressure": "150/95",
                "heart_rate": 95,
                "blood_glucose": 180,
                "troponin": "elevated",
                "ekg": "abnormal",
            }
        ),
    }

    try:
        MedicalAssistants().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=sample_inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MedicalAssistants().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
