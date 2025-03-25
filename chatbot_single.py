import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Set up Gemini API
GEMINI_API_KEY = "AIzaSyAuEizIGbZlE_FMCfwbcdyHYBz6R8al6Ik"  # Replace with actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Fixed invoice PDF path
INVOICE_PDF_PATH = "invoice_templates/invoice_1.pdf"

# Ensure session state variables are initialized
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "invoice_text" not in st.session_state:
    st.session_state.invoice_text = None  # Placeholder for extracted text

# Function to extract text from invoice PDF
def extract_text_from_pdf(file_path):
    """Extracts text from a given PDF file path."""
    try:
        doc = fitz.open(file_path)  # Open PDF
        text = "\n".join([page.get_text() for page in doc])  # Extract text
        return text if text else "No text found in the invoice."
    except Exception as e:
        return f"Error reading PDF: {e}"

# Load invoice text once
if st.session_state.invoice_text is None:
    st.session_state.invoice_text = extract_text_from_pdf(INVOICE_PDF_PATH)

# Function to generate a response using Gemini AI
def generate_response(conversation_history, user_query, invoice_text):
    model = genai.GenerativeModel("gemini-1.5-pro")  # Ensure correct model name

    # Format chat history for context
    history_text = "\n".join(
        [f"User: {msg['user']}\nAI: {msg['ai']}" for msg in conversation_history]
    )

    # Construct the prompt
    prompt = f"""
    You are an AI chatbot that assists users with general queries.

    If the user asks about invoice details, use the following extracted invoice text:

    {invoice_text}  

    The conversation so far:

    {history_text}

    User's message:
    {user_query}

    Guidelines:
    - Answer normally if the question is not about the invoice.
    - If the user asks about previous messages, check the chat history and confirm.
    - Keep responses concise and avoid generating unnecessary details.
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response and response.text else "I couldn't generate a response."
    except Exception as e:
        return f"Error generating response: {e}"

# Function to run the chatbot
def run():
    """Runs the chatbot app."""
    st.title("💬 Single Invoice QnA Chatbot")

    # Ensure session state variable is initialized before using it
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Display chat history
    for msg in st.session_state.conversation:
        with st.chat_message("user"):
            st.write(msg["user"])
        with st.chat_message("assistant"):
            st.write(msg["ai"])

    # User input
    user_query = st.chat_input("Ask about the invoice...")

    if user_query:
        response = generate_response(
            st.session_state.conversation,
            user_query,
            st.session_state.invoice_text
        )

        # Store chat history
        st.session_state.conversation.append({"user": user_query, "ai": response})

        # Display new messages
        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            st.write(response)

# Run the chatbot when executed directly
if __name__ == "__main__":
    run()
