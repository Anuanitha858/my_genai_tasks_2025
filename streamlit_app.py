import streamlit as st
import os
import json
from invoice import extract_text_from_pdf, extract_invoice_with_gemini, save_data_as_json

# Streamlit App
def run():  
    st.title("📄 Invoice Data Extractor")
    st.write("Upload an invoice PDF to extract structured data using Gemini AI.")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload an invoice PDF", type="pdf")

    # Gemini API key input
    api_key = "AIzaSyAuEizIGbZlE_FMCfwbcdyHYBz6R8al6Ik"  # Example API key

    if uploaded_file and api_key:
        # Save the uploaded file temporarily
        temp_pdf_path = "temp_invoice.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Extract text from the PDF
        text = extract_text_from_pdf(temp_pdf_path)

        # Display extracted text (optional)
        with st.expander("View Extracted Text"):
            st.write(text)

        # Extract invoice details using Gemini AI
        st.write("Extracting invoice details...")
        try:
            invoice_data = extract_invoice_with_gemini(text, api_key)

            if invoice_data:
                # Try to parse the cleaned response into JSON
                json_data = json.loads(invoice_data)
                st.success("Invoice data extracted successfully!")
                
                # Display the JSON data
                st.subheader("Extracted Invoice Data")
                st.json(json_data)

                # Save the JSON data to a file
                output_json_path = "invoice_data.json"
                save_data_as_json(json_data, output_json_path)
                
                # Provide a download link for the JSON file
                with open(output_json_path, "rb") as f:
                    st.download_button(
                        label="Download JSON",
                        data=f,
                        file_name="invoice_data.json",
                        mime="application/json"
                    )
        except Exception as e:
            st.error(f"Error: {e}")

        # Clean up the temporary PDF file
        os.remove(temp_pdf_path)
