# pages/images.py - Image upload page
import streamlit as st
from PIL import Image
from datetime import datetime
import io
from components.patient_info_display import display_patient_info
from components.navigation_buttons import render_navigation_buttons
from constants import IMAGE_TYPES, BODY_REGIONS


def render_images_page():
    st.title("Upload Medical Images")

    # Display patient info
    if st.session_state.patient_data:
        st.info(
            f"Patient: {st.session_state.patient_data.get('first_name', '')} {st.session_state.patient_data.get('last_name', '')} | ID: {st.session_state.patient_data.get('id', '')} | Age: {st.session_state.patient_data.get('age', '')}"
        )

    st.markdown(
        """
        Upload medical images for AI analysis. Supported formats:
        - X-rays (JPEG, PNG, DICOM)
        - CT Scans (DICOM)
        - MRI (DICOM)
        - Ultrasound images
        """
    )

    # Initialize image storage in session state if it doesn't exist
    if "uploaded_images" not in st.session_state:
        st.session_state.uploaded_images = []

    # Display existing uploaded images
    if st.session_state.uploaded_images:
        st.subheader("Uploaded Images")
        image_cols = st.columns(min(3, len(st.session_state.uploaded_images)))

        for idx, img_data in enumerate(st.session_state.uploaded_images):
            col_idx = idx % 3
            with image_cols[col_idx]:
                if img_data.get("file"):
                    try:
                        image = Image.open(io.BytesIO(img_data["file"]))
                        st.image(
                            image,
                            caption=f"{img_data['type']} - {img_data['date']}",
                            use_container_width=True,
                        )
                        if st.button(f"Remove", key=f"remove_{idx}"):
                            st.session_state.uploaded_images.pop(idx)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error displaying image {idx+1}: {e}")

    # New image upload section
    st.subheader("Add New Image")

    col1, col2 = st.columns([2, 3])

    with col1:
        image_type = st.selectbox(
            "Image Type",
            [
                "Chest X-ray",
                "Brain MRI",
                "Abdominal CT",
                "Bone X-ray",
                "Ultrasound",
                "Other",
            ],
            index=0,
            key="new_image_type",
        )

        body_region = st.selectbox(
            "Body Region",
            ["Chest/Thorax", "Abdomen", "Head/Brain", "Spine", "Extremities", "Other"],
            index=(
                0
                if image_type == "Chest X-ray"
                else 2 if image_type == "Brain MRI" else 1
            ),
            key="new_body_region",
        )

        image_date = st.date_input(
            "Image Date", value=datetime.now(), key="new_image_date"
        )
        image_notes = st.text_area("Notes about the image", key="new_image_notes")

    with col2:
        uploaded_file = st.file_uploader(
            "Upload Medical Image",
            type=["jpg", "jpeg", "png", "dcm"],
            key="new_image_file",
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

                if st.button("Add This Image"):
                    # Save to session state
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    new_image = {
                        "file": buf.getvalue(),
                        "type": image_type,
                        "region": body_region,
                        "date": str(image_date),
                        "notes": image_notes,
                    }
                    st.session_state.uploaded_images.append(new_image)
                    st.success("Image added successfully!")
                    # Clear the uploader
                    # st.session_state.new_image_file = None
                    st.rerun()

            except Exception as e:
                st.error(f"Error processing image: {e}")

    st.divider()

    # Navigation buttons
    render_navigation_buttons(
        prev_page="Patient_Information", next_page="Symptoms_Lab_Results"
    )
