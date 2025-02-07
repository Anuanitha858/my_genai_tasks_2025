import fitz  # PyMuPDF
import google.generativeai as genai
import json

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    document = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        full_text += page.get_text("text")  # Extract text from each page
    return full_text

# Function to extract invoice details using Gemini AI
def extract_invoice_with_gemini(text, api_key):
    """
    Uses Gemini AI to extract structured invoice details from the provided text.
    """
    genai.configure(api_key=api_key)
    
    # Define the prompt for Gemini AI
    prompt = f"""
    Given the following invoice text:

    {text}

    Please extract the following details and return them in the JSON format:

    {{
        "invoice_details": {{
            "invoice_number": "<Invoice Number>",
            "order_number": "<Order Number>",
            "invoice_date": "<Invoice Date>",
            "due_date": "<Due Date>",
            "total_due": "<Total Due>"
        }},
        "sender_details": {{
            "name": "<Sender Name>",
            "address": "<Sender Address>",
            "email": "<Sender Email>"
        }},
        "recipient_details": {{
            "name": "<Recipient Name>",
            "address": "<Recipient Address>",
            "email": "<Recipient Email>"
        }},
        "items": [
            {{
                "quantity": "<Quantity>",
                "service": "<Service Description>",
                "rate": "<Rate>",
                "adjustment": "<Adjustment>",
                "sub_total": "<Sub Total>"
            }}
        ],
        "tax_details": {{
            "tax_amount": "<Tax Amount>"
        }},
        "bank_details": {{
            "bank_name": "<Bank Name>",
            "account_number": "<Account Number>",
            "bsb_number": "<BSB Number>"
        }}
    }}
    
    Please provide the result in JSON format as shown above.
    """
    
    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        # Generate the response from Gemini AI
        response = model.generate_content(prompt)
        
        # Log the raw response to check what is returned
        print("Raw Response from Gemini AI:", response.text)
        
        if not response.text.strip():
            raise ValueError("Empty response from Gemini AI.")
        
        # Clean up the response: remove backticks, "json", and unwanted characters
        clean_response = response.text.strip().lstrip("```json").rstrip("```").strip()
        
        # Log the cleaned response
        print("Cleaned Response from Gemini AI:", clean_response)
        
        return clean_response
    
    except Exception as e:
        print(f"Error during AI request: {e}")
        return None

# Function to save extracted data as JSON
def save_data_as_json(data, output_path):
    """
    Saves the extracted data as a JSON file.
    """
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Main function
def main():
    # Path to the invoice PDF
    pdf_path = "invoice_templates/invoice_1.pdf"  # Update the path to your invoice PDF
    output_json_path = pdf_path.split('.')[0]+".json"  # Output path for JSON file
    api_key = "AIzaSyAuEizIGbZlE_FMCfwbcdyHYBz6R8al6Ik"  # Your Gemini API ke

    # Step 1: Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Use Gemini AI to process the invoice and extract structured data
    invoice_data = extract_invoice_with_gemini(text, api_key)

    if invoice_data:
        # Step 3: Try to parse the cleaned response into JSON
        try:
            json_data = json.loads(invoice_data)
            save_data_as_json(json_data, output_json_path)
            print(f"Data saved to {output_json_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Response causing the error:", invoice_data)
    else:
        print("No valid response to parse.")

# Run the main function
if __name__ == "__main__":
    main()