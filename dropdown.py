import os
import time
import json
import re
import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
from streamlit_option_menu import option_menu
from streamlit_app import extract_text_from_pdf, extract_invoice_with_gemini, save_data_as_json

# Set up Gemini API
GEMINI_API_KEY = "AIzaSyAuEizIGbZlE_FMCfwbcdyHYBz6R8al6Ik"
genai.configure(api_key=GEMINI_API_KEY)

# Folder containing multiple invoices
INVOICE_FOLDER = "invoice_templates"

# Function to get a specific invoice file
def get_invoice_by_number(invoice_number):
    for file in os.listdir(INVOICE_FOLDER):
        if file.endswith(".pdf") and invoice_number in file:
            return os.path.join(INVOICE_FOLDER, file)
    return None

# Function to get the latest available invoice
def get_latest_invoice():
    pdf_files = sorted(
        [f for f in os.listdir(INVOICE_FOLDER) if f.endswith(".pdf")],
        reverse=True  
    )
    return os.path.join(INVOICE_FOLDER, pdf_files[0]) if pdf_files else None

# Function to generate a response using Gemini AI
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
            if response and response.candidates:
                return response.candidates[0].content.parts[0].text
            return "No valid response generated. Please try again later."
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)  
            else:
                return f"Error generating response: {e}. Please try again later."

# Initialize session state for chat history and invoice details
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "invoice_file" not in st.session_state:
    st.session_state.invoice_file = get_latest_invoice()
if "invoice_text" not in st.session_state and st.session_state.invoice_file:
    st.session_state.invoice_text = extract_text_from_pdf(st.session_state.invoice_file)

# Sidebar navigation with option_menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main menu",  # Optional, title for the menu
        options=["🏠 Home", "💬 Invoice Chatbot", "📄 Invoice Data Extractor"],  
        icons=["house", "chat", "file-earmark-text"],  # Choose appropriate icons
        menu_icon="cast",
        default_index=0,
    )

# Home Page
def home_page():
    st.title("🏠 Welcome to Invoice chatbot and Invoice data extractor")

# Invoice Chatbot
def invoice_chatbot():
    st.title("💬 Invoice Chatbot")

    for msg in st.session_state.conversation:
        with st.chat_message("user"):
            st.write(msg["user"])
        with st.chat_message("assistant"):
            st.write(msg["ai"])

    user_query = st.chat_input("Ask about the invoice...")

    if user_query:
        match = re.search(r"(INV-\d+|invoice\d+)", user_query, re.IGNORECASE)
        if match:
            invoice_number = match.group(1)
            new_invoice_file = get_invoice_by_number(invoice_number)
            if new_invoice_file:
                st.session_state.invoice_file = new_invoice_file
                st.session_state.invoice_text = extract_text_from_pdf(new_invoice_file)
                response = f"Loaded details for {invoice_number}. How can I assist?"
            else:
                response = f"No invoice found matching {invoice_number}. Please check the invoice number and try again."
        else:
            response = generate_response(
                st.session_state.conversation,
                user_query,
                st.session_state.invoice_text
            )

        st.session_state.conversation.append({"user": user_query, "ai": response})

        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            st.write(response)

# Invoice Data Extractor
def invoice_data_extractor():
    st.title("📄 Invoice Data Extractor")
    st.write("Upload an invoice PDF to extract structured data using Gemini AI.")

    uploaded_file = st.file_uploader("Upload an invoice PDF", type="pdf")

    if uploaded_file:
        temp_pdf_path = "temp_invoice.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        text = extract_text_from_pdf(temp_pdf_path)

        with st.expander("View Extracted Text"):
            st.write(text)

        st.write("Extracting invoice details...")
        try:
            invoice_data = extract_invoice_with_gemini(text, GEMINI_API_KEY)

            if invoice_data:
                json_data = json.loads(invoice_data)
                st.success("Invoice data extracted successfully!")
                
                st.subheader("Extracted Invoice Data")
                st.json(json_data)

                output_json_path = "invoice_data.json"
                save_data_as_json(json_data, output_json_path)

                with open(output_json_path, "rb") as f:
                    st.download_button(
                        label="Download JSON",
                        data=f,
                        file_name="invoice_data.json",
                        mime="application/json"
                    )
        except Exception as e:
            st.error(f"Error: {e}")

        os.remove(temp_pdf_path)

# Load selected app
if selected == "🏠 Home":
    home_page()
elif selected == "💬 Invoice Chatbot":
    invoice_chatbot()
elif selected == "📄 Invoice Data Extractor":
    invoice_data_extractor()
