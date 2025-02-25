# pages/images.py - Image upload page
import streamlit as st
from PIL import Image
from datetime import datetime
import io
from components.patient_info_display import display_patient_info
from components.navigation_buttons import render_navigation_buttons
from constants import IMAGE_TYPES, BODY_REGIONS


def render_images_page():
    """Render the medical image upload page"""
    st.title("Upload Medical Images")

    # Display patient info
    display_patient_info()

    st.markdown(
        """
    Upload medical images for AI analysis. Supported formats:
    - X-rays (JPEG, PNG, DICOM)
    - CT Scans (DICOM)
    - MRI (DICOM)
    - Ultrasound images
    """
    )

    col1, col2 = st.columns([2, 3])

    with col1:
        image_type = st.selectbox("Image Type", IMAGE_TYPES, index=0)

        # Set default body region based on image type
        default_index = 0
        if image_type == "Chest X-ray":
            default_index = 0
        elif image_type == "Brain MRI":
            default_index = 2
        elif image_type == "Abdominal CT":
            default_index = 1

        body_region = st.selectbox("Body Region", BODY_REGIONS, index=default_index)
        image_date = st.date_input("Image Date", value=datetime.now())
        image_notes = st.text_area("Notes about the image")

    with col2:
        uploaded_file = st.file_uploader(
            "Upload Medical Image", type=["jpg", "jpeg", "png", "dcm"]
        )

        if uploaded_file is not None:
            try:
                # Display the image
                image = Image.open(uploaded_file)
                st.image(
                    image,
                    caption=f"{image_type} - {image_date}",
                    use_container_width=True,
                )

                # Save to session state
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.session_state.uploaded_image = {
                    "file": buf.getvalue(),
                    "type": image_type,
                    "region": body_region,
                    "date": str(image_date),
                    "notes": image_notes,
                }

                st.success("Image uploaded successfully!")
            except Exception as e:
                st.error(f"Error processing image: {e}")

    # Navigation buttons
    render_navigation_buttons(prev_page="patient", next_page="symptoms")
