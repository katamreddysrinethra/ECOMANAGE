import streamlit as st
import google.generativeai as genai
from PIL import Image


# ==========================================
# CONFIGURE GEMINI
# ==========================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


# ==========================================
# AI ANALYSIS
# ==========================================

def analyze_waste(image):

    prompt = """
    You are a waste management expert.

    Analyze the uploaded image and provide:

    1. Waste Type
    2. Category
    3. Recyclable (Yes/No)
    4. Recommended Bin
    5. Hazard Level
    6. Disposal Recommendation
    7. Estimated Reward Points (1-25)
    8. Environmental Impact
    9. Educational Fact

    Format response clearly.
    """

    response = model.generate_content(
        [
            prompt,
            image
        ]
    )

    return response.text


# ==========================================
# PAGE
# ==========================================

def ai_scanner_page():

    st.title("🤖 AI Waste Scanner")

    st.info(
        """
        Upload a waste image and let AI identify
        the waste type and provide disposal guidance.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload Waste Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_file:

        image = Image.open(
            uploaded_file
        )

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        if st.button(
            "🔍 Scan Waste"
        ):

            with st.spinner(
                "Analyzing image..."
            ):

                result = analyze_waste(
                    image
                )

            st.success(
                "Analysis Complete"
            )

            st.markdown(result)