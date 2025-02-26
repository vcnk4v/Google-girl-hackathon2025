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


def test():
    """
    Test the crew execution and returns the results.
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
        MedicalAssistants().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=sample_inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
