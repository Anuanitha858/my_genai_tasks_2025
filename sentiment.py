import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini AI
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")

# Function to analyze sentiment
def analyze_sentiment(review_type, review_text):
    sentiment_prompt = f"""
    You are an AI that analyzes sentiment in {review_type.lower()}.
    Classify the sentiment as **Positive**, **Neutral**, or **Negative** based on the review provided.

    **Review:**
    {review_text}

    **Response Format (Strict JSON):**
    {{
        "sentiment": "Positive"   # or "Neutral" or "Negative"
    }}
    """

    try:
        response = model.generate_content(sentiment_prompt)
        return json.loads(response.text) if response else {"sentiment": "Error: No response generated."}
    except Exception as e:
        return {"sentiment": f"Error: {e}"}

# Function to run the Streamlit app
def run():
    """Runs the Sentiment Analysis app."""
    st.title("🎭🍽 Sentiment Analysis for Food and Film Reviews")
    st.write("Analyze Film or Food Reviews to determine their sentiment (Positive, Neutral, Negative).")

    # Select type of review
    review_type = st.radio("Choose Review Type:", ["🎬 Film Review", "🍔 Food Review"])

    # User input
    review_text = st.text_area("Enter the review text:", "", height=200)

    if st.button("Analyze Sentiment"):
        if review_text.strip() == "":
            st.warning("Please enter a review.")
        else:
            sentiment_result = analyze_sentiment(review_type, review_text)

            # Display sentiment result in JSON format
            st.subheader("📌 Sentiment Analysis Result (JSON):")
            st.json(sentiment_result)

# Run the app when executed directly
if __name__ == "__main__":
    run()
