import json
import os
from datetime import datetime
from dotenv import load_dotenv
from medical_assistants.src.medical_assistants.crew import MedicalAssistants
import re
import uuid
from google import genai
from google.genai import types
import PIL.Image


class ImageAnalyzer:
    def __init__(self):
        pass

    def analyze_image(self, image_metadata):
        """
        Analyze a medical image and return insights.

        Args:
            image_path (str): The path to the image file

        Returns:
            dict: The analysis results
        """
        image = PIL.Image.open(image_metadata.get("full_path"))
        image_notes = image_metadata.get("notes", "")
        image_region = image_metadata.get("region", "")
        image_type = image_metadata.get("type", "")
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                f"You are an expert in medical imaging with specialization in radiology, cardiology, and general diagnostic imaging. You analyze {image_type} images to identify abnormalities, potential conditions, and provide supporting evidence for diagnoses in the region {image_region}. You're precise in your observations and only report findings that are clearly visible in the images. Your analysis includes anatomical descriptions, abnormality characterization, and clinical significance. You always maintain confidentiality and adhere to medical ethics guidelines. Some extra notes are {image_notes}.",
                image,
            ],
        )

        return {
            # "image_path": image_metadata.get("path"),
            "findings": response.text,
        }

    def analyze_multiple_images(self, image_metadata):
        """
        Analyze multiple medical images and return insights.

        Args:
            image_paths (list): List of image file paths

        Returns:
            list: List of analysis results for each image
        """
        return [
            self.analyze_image(image_metadata_unit)
            for image_metadata_unit in image_metadata
        ]


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
        image_metadata = self._save_image_metadata(case_id, uploaded_images)

        return {
            "case_id": case_id,
            "data_package": data_package,
            "image_metadata": image_metadata,
        }

    def run_diagnosis(self, case_id, data_package, image_metadata):
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

        image_results = ImageAnalyzer().analyze_multiple_images(image_metadata)

        # Format inputs for CrewAI
        inputs = {
            "patient_data": json.dumps(patient_data),
            "symptoms": json.dumps(symptoms),
            "lab_results": json.dumps(lab_results),
            "image_results": json.dumps(image_results),
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
        image_paths = []
        case_dir = os.path.join(self.data_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)

        # Create an images directory
        images_dir = os.path.join(case_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        # Save metadata about each image
        image_metadata = []

        for i, img_data in enumerate(uploaded_images):
            # Generate a unique filename for the image
            filename = f"image_{i}_{uuid.uuid4().hex[:8]}.png"
            file_path = os.path.join(images_dir, filename)

            # Save the actual image file
            with open(file_path, "wb") as img_file:
                img_file.write(img_data.get("file"))

            # Store the relative path for use within the application
            relative_path = os.path.join("images", filename)

            # Extract metadata (excluding the binary file data)
            metadata = {
                "index": i,
                "type": img_data.get("type"),
                "region": img_data.get("region"),
                "date": img_data.get("date"),
                "notes": img_data.get("notes"),
                "filename": filename,
                "path": relative_path,
                "full_path": file_path,
            }
            image_metadata.append(metadata)
            image_paths.append(file_path)

        # Save the metadata list
        with open(os.path.join(images_dir, "image_metadata.json"), "w") as f:
            json.dump(image_metadata, f, indent=4)

        return image_metadata

    def _save_diagnostic_results(self, case_id, diagnosis):
        """Save the diagnostic results to a JSON file."""
        case_dir = os.path.join(self.data_dir, case_id)
        os.makedirs(case_dir, exist_ok=True)

        # Save the diagnosis
        with open(os.path.join(case_dir, "diagnosis.json"), "w") as f:
            json.dump(diagnosis, f, indent=4)
