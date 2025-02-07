import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini AI
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")

# Supported languages
LANGUAGES = {
    "Auto-Detect": "auto",
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
}

# Streamlit App
def run():
    st.title("🌍 Language Detection & Translation")

    # Select mode
    task = st.selectbox("Choose Task:", ["🔍 Detect Language", "🌐 Translate Text"])

    # User input
    text_input = st.text_area("Enter text:", "", height=150)

    if task == "🔍 Detect Language":
        if st.button("Detect Language"):
            if text_input.strip() == "":
                st.warning("Please enter some text.")
            else:
                detection_prompt = f"""
                Detect the language of the following text and return a JSON response.

                **Text:**
                {text_input}

                **Response Format (Strict JSON):**
                {{
                    "detected_language": "Language Name"
                }}
                """
                response = model.generate_content(detection_prompt)

                # Check if response is not empty and valid JSON
                if response and response.text.strip():  # Check if response is not empty
                    try:
                        detection_result = json.loads(response.text.strip())
                        st.subheader("📌 Detected Language:")
                        st.json(detection_result)  # Display JSON response

                    except json.JSONDecodeError:
                        st.error("⚠️ Failed to decode JSON. AI response might not be structured correctly.")
                        st.text("Raw Response:")
                        st.write(response.text)  # Display raw response if decoding fails
                else:
                    st.error("⚠️ No response received from AI.")

    elif task == "🌐 Translate Text":
        col1, col2 = st.columns(2)
        with col1:
            source_language = st.selectbox("Select Source Language:", list(LANGUAGES.keys()))
        with col2:
            target_language = st.selectbox("Select Target Language:", list(LANGUAGES.keys()))

        if st.button("Translate"):
            if text_input.strip() == "":
                st.warning("Please enter some text.")
            else:
                translation_prompt = f"""
                Translate the following text from {source_language} to {target_language} and return a JSON response.

                **Text:**
                {text_input}

                **Response Format (Strict JSON):**
                {{
                    "translated_text": "Translated text in {target_language}"
                }}
                """
                response = model.generate_content(translation_prompt)

                # Check if response is not empty and valid JSON
                if response and response.text.strip():  # Check if response is not empty
                    try:
                        translation_result = json.loads(response.text.strip())
                        st.subheader("📌 Translated Text:")
                        st.json(translation_result)  # Display JSON response

                    except json.JSONDecodeError:
                        st.error("⚠️ Failed to decode JSON. AI response might not be structured correctly.")
                        st.text("Raw Response:")
                        st.write(response.text)  # Display raw response if decoding fails
                else:
                    st.error("⚠️ No response received from AI.")

# Run the app when executed directly
if __name__ == "__main__":
    run()
