import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import json

def load_invoice():
    """Loads a single invoice JSON file."""
    try:
        with open("invoice.json", "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading invoice: {e}")
        return None

def process_invoice_query(query, invoice_data):
    """Processes user query based on invoice data."""
    response = "Sorry, I couldn't find relevant details."
    for key, value in invoice_data.items():
        if query.lower() in key.lower():
            response = f"{key}: {value}"
            break
    return response

def chatbot():
    st.title("Single Invoice Chatbot")
    
    invoice_data = load_invoice()
    if invoice_data is None:
        return
    
    user_input = st.text_input("Ask about the invoice:")
    if st.button("Submit"):
        response = process_invoice_query(user_input, invoice_data)
        st.write(response)

if __name__ == "__main__":
    chatbot()
