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

# # Function to generate a summary using Gemini AI
# def generate_summary(text_input):
#     summary_prompt = f"""
#     Summarize the following text into **clear and concise key points**, ensuring the essence of the content is retained.  
    
#     **Text to Summarize:**
#     {text_input}

#     **Expected Summary Format:**
#     - **Main Idea:** [One sentence summarizing the core message]  
#     - **Key Points:**  
#       - **Highlight 1**  
#       - **Highlight 2**  
#       - **Highlight 3**  
#     - **Conclusion:** [Final takeaway message]  

#     **Summary:**  
#     """
    
#     try:
#         response = model.generate_content(summary_prompt)
#         return response.text.strip() if response else "Error: No summary generated."
#     except Exception as e:
#         return f"Error generating summary: {e}"

# # Function to run the summarization app
# def run():
#     """Runs the Streamlit summarization app."""
#     st.title("📄 Text Summarization")
#     st.write("Enter a paragraph and get a **concise summary with key highlights**.")

#     # Medium-sized text area
#     text_input = st.text_area("Enter the text to summarize:", "", height=200)

#     if st.button("Summarize"):
#         if text_input.strip() == "":
#             st.warning("Please enter some text.")
#         else:
#             summary_text = generate_summary(text_input)
#             st.subheader("📌 Summary:")
#             st.write(summary_text)

# # Run the app when executed directly
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

# Function to generate a summary using Gemini AI
def generate_summary(text_input):
    summary_prompt = f"""
    Summarize the following text into **clear and concise key points**, ensuring the essence of the content is retained.  
    
    **Text to Summarize:**
    {text_input}

    **Expected Summary Format:**
    - **Main Idea:** [One sentence summarizing the core message]  
    - **Key Points:**  
      - **Highlight 1**  
      - **Highlight 2**  
      - **Highlight 3**  
    - **Conclusion:** [Final takeaway message]  

    **Summary:**  
    """
    
    try:
        response = model.generate_content(summary_prompt)
        return response.text.strip() if response else "Error: No summary generated."
    except Exception as e:
        return f"Error generating summary: {e}"

# Function to run the summarization app
def run():
    """Runs the Streamlit summarization app."""
    st.title("📄 Text Summarization")
    st.write("Enter a paragraph and get a **concise summary with key highlights**.")

    # Medium-sized text area
    text_input = st.text_area("Enter the text to summarize:", "", height=200)

    if st.button("Summarize"):
        if text_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            summary_text = generate_summary(text_input)
            st.subheader("📌 Summary:")
            st.write(summary_text)

# Run the app when executed directly
if __name__ == "__main__":
    run()
