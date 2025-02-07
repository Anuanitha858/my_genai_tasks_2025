import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini AI
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")

# Grammar Correction App
def run():
    st.title("🔤 Grammar and Spelling Correction")
    st.write("Enter grammatically incorrect text or text with spelling mistakes, and the app will return the corrected version.")

    # User input
    text_input = st.text_area("Enter the text to correct:", "", height=150)

    if st.button("Correct Text"):
        if text_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            # Create the prompt for correction
            correction_prompt = f"""
            Correct the following text for grammar and spelling mistakes. Ensure the corrected version is clear, grammatically correct, and properly spelled:

            **Original Text:**
            {text_input}

            **Corrected Text:**
            """

            # Request correction from the model
            response = model.generate_content(correction_prompt)

            if response and response.text.strip():  # Check if response is not empty
                try:
                    corrected_text = response.text.strip()
                    st.subheader("📌 Corrected Text:")
                    st.write(corrected_text)  # Display corrected text
                except Exception as e:
                    st.error(f"Error processing response: {e}")
            else:
                st.error("⚠️ No response received from AI.")

# Run the app when executed directly
if __name__ == "__main__":
    run()