import streamlit as st
import os
from datetime import date

from database.db import add_pickup_request


# ==========================================
# UPLOAD CONFIGURATION
# ==========================================

UPLOAD_FOLDER = "uploads/waste_images"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================
# SAVE IMAGE
# ==========================================

def save_uploaded_image(uploaded_file):

    if uploaded_file is None:
        return ""

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    return file_path


# ==========================================
# MAIN PAGE
# ==========================================

def pickup_request_page():

    st.title("📦 Waste Pickup Request")

    st.info(
        """
        Submit a pickup request for waste collection.

        A collector will review and accept your request.
        Once completed, you will earn reward points.
        """
    )

    with st.form(
        "pickup_request_form",
        clear_on_submit=True
    ):

        # ==================================
        # WASTE TYPE
        # ==================================

        waste_type = st.selectbox(
            "Waste Type *",
            [
                "Plastic",
                "Paper",
                "Food",
                "E-Waste",
                "Glass",
                "Metal",
                "Hazardous",
                "Other"
            ]
        )

        # ==================================
        # QUANTITY
        # ==================================

        quantity = st.number_input(
            "Quantity (kg)",
            min_value=0.0,
            step=0.5,
            value=1.0
        )

        # ==================================
        # PICKUP DATE
        # ==================================

        pickup_date = st.date_input(
            "Pickup Date *",
            min_value=date.today()
        )

        # ==================================
        # NOTES
        # ==================================

        notes = st.text_area(
            "Additional Notes (Optional)",
            placeholder=
            "Provide any special instructions..."
        )

        # ==================================
        # IMAGE
        # ==================================

        uploaded_image = st.file_uploader(
            "Upload Waste Image (Optional)",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        # ==================================
        # PREVIEW IMAGE
        # ==================================

        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption="Uploaded Waste Image",
                use_column_width=True
            )



         # ==============================
         # SUBMIT BUTTON
         # ==============================

        submit = st.form_submit_button(
        "🚛 Submit Pickup Request"
        )
        if submit:
            citizen_id = st.session_state.user["id"]
            image_path = save_uploaded_image(
                uploaded_image
                )
            add_pickup_request(
                citizen_id,
                waste_type,
                quantity,
                notes,
                str(pickup_date),
                image_path
                )
            st.success(
                "Pickup request submitted successfully!"
                )
            st.balloons()