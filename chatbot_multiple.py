import streamlit as st
import os
import time
import re
import fitz  # PyMuPDF
import google.generativeai as genai

# Set up Gemini API
GEMINI_API_KEY = "AIzaSyAuEizIGbZlE_FMCfwbcdyHYBz6R8al6Ik"
genai.configure(api_key=GEMINI_API_KEY)

# Folder containing multiple invoices
INVOICE_FOLDER = "invoice_templates"

def get_invoice_by_number(invoice_number):
    pdf_files = [f for f in os.listdir(INVOICE_FOLDER) if f.endswith(".pdf")]
    for file in pdf_files:
        if invoice_number in file:
            return os.path.join(INVOICE_FOLDER, file)
    return None

def get_latest_invoice():
    pdf_files = sorted(
        [f for f in os.listdir(INVOICE_FOLDER) if f.endswith(".pdf")],
        reverse=True
    )
    return os.path.join(INVOICE_FOLDER, pdf_files[0]) if pdf_files else None

def extract_text_from_pdf(file_path):
    """Extracts text from a given PDF file path."""
    try:
        doc = fitz.open(file_path)  
        text = "\n".join([page.get_text() for page in doc])  
        return text if text else "No text found in the invoice."
    except Exception as e:
        return f"Error reading PDF: {e}"

def generate_response(conversation_history, user_query, invoice_text):
    model = genai.GenerativeModel("gemini-pro")
    history_text = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" for msg in conversation_history])
    
    prompt = f"""
    You are an AI chatbot that assists users with invoice-related queries.
    
    Extracted Invoice Details:
    {invoice_text}

    Conversation History:
    {history_text}

    User's Query:
    {user_query}
    """

    for attempt in range(3):  
        try:
            response = model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "No valid response generated. Please try again later."
        except Exception as e:
            if attempt < 2:  
                time.sleep(2 ** attempt)
            else:
                return f"Error generating response: {e}. Please try again later."

# Initialize session state if not present
if "conversation" not in st.session_state:
    st.session_state.conversation = {}
if "invoice_file" not in st.session_state:
    st.session_state.invoice_file = get_latest_invoice()
if "invoice_text" not in st.session_state and st.session_state.invoice_file:
    st.session_state.invoice_text = extract_text_from_pdf(st.session_state.invoice_file)

def run():
    st.title("💬 Multiple QnA Invoice Chatbot")

    current_invoice = st.session_state.invoice_file
    if current_invoice not in st.session_state.conversation:
        st.session_state.conversation[current_invoice] = []

    # Display conversation history only for the selected invoice
    for msg in st.session_state.conversation[current_invoice]:
        with st.chat_message("user"):
            st.write(msg["user"])
        with st.chat_message("assistant"):
            st.write(msg["ai"])

    user_query = st.chat_input("Ask about the invoice...")

    if user_query:
        match = re.search(r"(INV-\\d+|invoice\\d+)", user_query, re.IGNORECASE)
        if match:
            invoice_number = match.group(1)
            new_invoice_file = get_invoice_by_number(invoice_number)
            if new_invoice_file:
                st.session_state.invoice_file = new_invoice_file
                st.session_state.invoice_text = extract_text_from_pdf(new_invoice_file)
                if new_invoice_file not in st.session_state.conversation:
                    st.session_state.conversation[new_invoice_file] = []
                response = f"Loaded details for {invoice_number}. How can I assist?"
            else:
                response = f"No invoice found matching {invoice_number}. Please check the invoice number and try again."
        else:
            response = generate_response(
                st.session_state.conversation[current_invoice], 
                user_query, 
                st.session_state.invoice_text
            )

        # Append conversation to session state specific to the invoice
        st.session_state.conversation[current_invoice].append({"user": user_query, "ai": response})

        # Display the user input and assistant response
        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    run()
