# import streamlit as st
# import google.generativeai as gen_ai
# from dotenv import load_dotenv
# import os
# import re
# import json  # Import json module for parsing

# def run():
#     # Load environment variables
#     load_dotenv()
#     GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#     # Configure Gemini-Pro
#     gen_ai.configure(api_key=GOOGLE_API_KEY)
#     model = gen_ai.GenerativeModel('gemini-pro')

#     st.title("Email-Spam Detection")

#     # Define strict JSON output in the prompt
#     prompt = '''
#     You are an AI-powered email spam detector. Your task is to analyze the given email content and classify it as either "Spam" or "Not Spam (Ham)".
    
#     ### **Guidelines**:
#     1. **Spam Identification**: If the email contains promotional offers, phishing attempts, scams, or excessive use of spam trigger words (e.g., "free", "win", "urgent", "claim now"), classify it as **Spam**.
#     2. **Not Spam (Ham) Identification**: If the email is a regular, professional, or personal message without spam characteristics, classify it as **Not Spam**.
#     3. **Strict Output Format**: Return the result in **valid JSON format only**, with no additional text. Example:
    
#     ```json
#     {"email_type": "Spam"}
#     ```
#     Ensure the response is valid JSON with no extra text.
#     '''

#     email_text = st.text_area("Enter the email content:", "")

#     if st.button("Detect Spam or Ham"):  # Updated button text
#         if email_text.strip() == "":
#             st.warning("Please enter some text.")
#         else:
#             full_prompt = f'{prompt}\n\nEmail Content:\n"{email_text}"\n\nReturn JSON output:'
#             response = model.generate_content(full_prompt)

#             if response and response.text:
#                 raw_response = response.text.strip()

#                 # Extract JSON using regex
#                 match = re.search(r'\{.*\}', raw_response, re.DOTALL)
#                 if match:
#                     json_content = match.group(0)
#                     try:
#                         email_classifier = json.loads(json_content)
#                         st.json(email_classifier)  # Display as JSON
#                     except json.JSONDecodeError:
#                         st.error("Failed to parse response as JSON. Response might be incorrectly formatted.")
#                         st.write(raw_response)  # Show raw response for debugging
#                 else:
#                     st.error("No valid JSON detected in the response. Check the AI output.")
#                     st.write(raw_response)  # Show raw response for debugging

# # Run the Streamlit app
# if __name__ == "__main__":
#     run()

import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv
import os
import re
import json  # Import json module for parsing

def run():
    # Load environment variables
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Configure Gemini-Pro
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel('gemini-1.5-pro')

    st.title("Email-Spam Detection")

    # Define strict JSON output in the prompt
    prompt = '''
    You are an AI-powered email spam detector. Your task is to analyze the given email content and classify it as either "Spam" or "Not Spam (Ham)".
    
    ### **Guidelines**:
    1. **Spam Identification**: If the email contains promotional offers, phishing attempts, scams, or excessive use of spam trigger words (e.g., "free", "win", "urgent", "claim now"), classify it as **Spam**.
    2. **Not Spam (Ham) Identification**: If the email is a regular, professional, or personal message without spam characteristics, classify it as **Not Spam**.
    3. **Strict Output Format**: Return the result in **valid JSON format only**, with no additional text. Example:
    
    ```json
    {"email_type": "Spam"}
    ```
    Ensure the response is valid JSON with no extra text.
    '''

    email_text = st.text_area("Enter the email content:", "")

    if st.button("Detect Spam or Ham"):  # Updated button text
        if email_text.strip() == "":
            st.warning("Please enter some text.")
        else:
            full_prompt = f'{prompt}\n\nEmail Content:\n"{email_text}"\n\nReturn JSON output:'
            response = model.generate_content(full_prompt)

            if response and response.text:
                raw_response = response.text.strip()

                # Extract JSON using regex
                match = re.search(r'\{.*\}', raw_response, re.DOTALL)
                if match:
                    json_content = match.group(0)
                    try:
                        email_classifier = json.loads(json_content)
                        st.json(email_classifier)  # Display as JSON
                    except json.JSONDecodeError:
                        st.error("Failed to parse response as JSON. Response might be incorrectly formatted.")
                        st.write(raw_response)  # Show raw response for debugging
                else:
                    st.error("No valid JSON detected in the response. Check the AI output.")
                    st.write(raw_response)  # Show raw response for debugging

# Run the Streamlit app
if __name__ == "__main__":
    run()
