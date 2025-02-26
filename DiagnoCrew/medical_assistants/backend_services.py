import json
import os
from datetime import datetime
from dotenv import load_dotenv
from medical_assistants.src.medical_assistants.crew import MedicalAssistants
import re


class DiagnosticService:
    """
    Service class that handles diagnostic data and processing.
    This will serve as the interface between Streamlit frontend
    and any external services like CrewAI.
    """

    def __init__(self, data_dir="diagnostic_data"):
        """Initialize the diagnostic service with a data directory for storing patient data."""
        self.data_dir = data_dir
        # Create the data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

    def process_output(self, output):
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

    def process_diagnostic_data(
        self,
        patient_data,
        uploaded_images,
        symptoms,
        lab_results,
        chief_complaint=None,
        additional_symptoms=None,
        onset_info=None,
    ):
        """
        Process diagnostic data and prepare it for external analysis.

        Args:
            patient_data (dict): Patient demographic and medical history information
            uploaded_images (list): List of dictionaries containing image data and metadata
            symptoms (list): List of selected symptoms
            lab_results (dict): Dictionary of lab test results
            chief_complaint (str, optional): Patient's primary complaint
            additional_symptoms (str, optional): Additional symptoms not in the checklist
            onset_info (dict, optional): Information about symptom onset and duration

        Returns:
            dict: The processed diagnostic data and a unique case ID
        """
        # Generate a case ID
        case_id = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{patient_data.get('id', 'UNKNOWN')}"

        # Prepare the data package
        data_package = {
            "case_id": case_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_data": patient_data,
            "symptoms": {
                "chief_complaint": chief_complaint,
                "symptom_list": symptoms,
                "additional_symptoms": additional_symptoms,
                "onset_info": onset_info,
            },
            "lab_results": lab_results,
            "image_count": len(uploaded_images) if uploaded_images else 0,
        }

        # Save the data package to a JSON file (excluding actual image data for now)
        self._save_diagnostic_data(case_id, data_package)

        # In a real implementation, you would process the images separately
        # and perhaps store them in a different way or format
        self._save_image_metadata(case_id, uploaded_images)

        return {"case_id": case_id, "data_package": data_package}

    def run_diagnosis(self, case_id, data_package):
        """
        Run the diagnostic analysis. This is where you would integrate with CrewAI.

        Args:
            case_id (str): The unique case identifier
            data_package (dict): The prepared diagnostic data

        Returns:
            dict: The diagnostic results
        """

        load_dotenv()
        patient_data = data_package["patient_data"]
        symptoms = data_package["symptoms"]
        lab_results = data_package["lab_results"]

        # Format inputs for CrewAI
        inputs = {
            "patient_data": json.dumps(patient_data),
            "symptoms": json.dumps(symptoms),
            "lab_results": json.dumps(lab_results),
        }

        try:
            # Run the CrewAI medical assistants
            crew_result = (MedicalAssistants().crew().kickoff(inputs=inputs)).raw

            # Parse the result
            if isinstance(crew_result, str):
                try:

                    diagnosis = self.process_output(crew_result)

                except:
                    diagnosis = {
                        "case_id": case_id,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "error": "Could not parse result as JSON",
                        "raw_result": crew_result,
                    }
            else:
                diagnosis = crew_result

            # Add case ID and timestamp if not present
            diagnosis["case_id"] = case_id
            diagnosis["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self._save_diagnostic_results(case_id, diagnosis)

            return diagnosis
        except Exception as e:
            # Handle any exceptions
            error_diagnosis = {
                "case_id": case_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": f"An error occurred while running the diagnosis: {str(e)}",
            }
            self._save_diagnostic_results(case_id, error_diagnosis)
            return error_diagnosis

    def _save_diagnostic_data(self, case_id, data_package):
        """Save the diagnostic data package to a JSON file."""
        case_dir = os.path.join(self.data_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)

        # Save the data package
        with open(os.path.join(case_dir, "data_package.json"), "w") as f:
            json.dump(data_package, f, indent=4)

    def _save_image_metadata(self, case_id, uploaded_images):
        """Save metadata about uploaded images."""
        if not uploaded_images:
            return

        case_dir = os.path.join(self.data_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)

        # Create an images directory
        images_dir = os.path.join(case_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        # Save metadata about each image
        image_metadata = []
        for i, img_data in enumerate(uploaded_images):
            # Extract metadata (excluding the binary file data)
            metadata = {
                "index": i,
                "type": img_data.get("type"),
                "region": img_data.get("region"),
                "date": img_data.get("date"),
                "notes": img_data.get("notes"),
            }
            image_metadata.append(metadata)

            # In a real implementation, weyou would save the actual image file here
            # For now, we'll just note that we're skipping this to keep things simple

        # Save the metadata list
        with open(os.path.join(images_dir, "image_metadata.json"), "w") as f:
            json.dump(image_metadata, f, indent=4)

    def _save_diagnostic_results(self, case_id, diagnosis):
        """Save the diagnostic results to a JSON file."""
        case_dir = os.path.join(self.data_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)

        # Save the diagnosis
        with open(os.path.join(case_dir, "diagnosis.json"), "w") as f:
            json.dump(diagnosis, f, indent=4)
