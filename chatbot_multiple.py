import streamlit as st
import json

def load_invoices():
    """Loads multiple invoices from a JSON file."""
    try:
        with open("invoices.json", "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading invoices: {e}")
        return []

def process_invoice_query(query, invoices):
    """Searches through multiple invoices for relevant details."""
    results = []
    for invoice in invoices:
        for key, value in invoice.items():
            if query.lower() in key.lower():
                results.append(f"Invoice {invoice.get('invoice_id', 'Unknown')}: {key} - {value}")
    return results if results else ["No relevant details found."]

def chatbot():
    st.title("Multiple Invoices Chatbot")
    
    invoices = load_invoices()
    if not invoices:
        return
    
    user_input = st.text_input("Ask about invoices:")
    if st.button("Submit"):
        responses = process_invoice_query(user_input, invoices)
        for response in responses:
            st.write(response)

if __name__ == "__main__":
    chatbot()
