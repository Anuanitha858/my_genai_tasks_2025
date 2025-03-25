# import streamlit as st
# import google.generativeai as gen_ai
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # Configure Gemini AI
# gen_ai.configure(api_key=GOOGLE_API_KEY)
# model = gen_ai.GenerativeModel("gemini-pro")

# # Streamlit App for Content Generation
# def run():  
#     st.title("📝 Content Generation")

#     # User input for topic and specifications
#     topic = st.text_input("Enter Topic:")
#     specifications = st.text_area("Enter Specifications (format, structure, tone, keywords):", "", height=150)

#     if st.button("Generate"):
#         if topic.strip() == "" or specifications.strip() == "":
#             st.warning("Please enter both topic and specifications.")
#         else:
#             generation_prompt = f"""
#             Generate content based on the given topic and specifications.

#             **Topic**: {topic}

#             **Specifications**:
#             {specifications}

#             **Response Format**:
#             - Provide the content with structure, tone, and elements as per the specifications.
#             """
#             response = model.generate_content(generation_prompt)

#             try:
#                 content_result = response.text.strip()
#                 st.subheader(f"📌 Generated Content:")
#                 st.write(content_result)

#             except Exception as e:
#                 st.error(f"Error generating content: {e}")

# # Run the app
# if __name__ == "__main__":
#     run()
import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini AI
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-1.5-pro")

# Streamlit App for Content Generation
def run():  
    st.title("📝 Content Generation")

    # User input for topic and specifications
    topic = st.text_input("Enter Topic:")
    specifications = st.text_area("Enter Specifications (format, structure, tone, keywords):", "", height=150)

    if st.button("Generate"):
        if topic.strip() == "" or specifications.strip() == "":
            st.warning("Please enter both topic and specifications.")
        else:
            generation_prompt = f"""
            Generate content based on the given topic and specifications.

            **Topic**: {topic}

            **Specifications**:
            {specifications}

            **Response Format**:
            - Provide the content with structure, tone, and elements as per the specifications.
            """
            response = model.generate_content(generation_prompt)

            try:
                content_result = response.text.strip()
                st.subheader(f"📌 Generated Content:")
                st.write(content_result)

            except Exception as e:
                st.error(f"Error generating content: {e}")

# Run the app
if __name__ == "__main__":
    run()
