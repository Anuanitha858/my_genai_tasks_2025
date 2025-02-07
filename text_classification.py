import streamlit as st
import pandas as pd

def run():
    # Streamlit UI
    st.title("Text Classification")

    # Define keywords for each category
    categories_keywords = {
        "Technology": ["AI", "machine learning", "chip", "software", "hardware", "technology", "computer", "innovation", "cloud", "app"],
        "Finance": ["stocks", "investment", "market", "banking", "finance", "economy", "interest rates", "credit", "loan", "capital"],
        "Medical": ["health", "hospital", "doctor", "treatment", "medicine", "surgery", "diagnosis", "patient", "disease", "care"],
        "Agriculture": ["farming", "crops", "harvest", "agriculture", "farm", "soil", "irrigation", "livestock", "pesticide", "fertilizer"]
    }

    # Function to classify the text based on keywords
    def classify_text(text):
        # Normalize the text to lowercase
        text = text.lower()

        # Check each category for keyword presence
        for category, keywords in categories_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    return category
        return "Uncategorized"  # If no category matches

    # Input text field
    input_text = st.text_area("Enter text to classify:", "")

    if st.button("Classify"):  # Button to classify the text
        if input_text.strip() == "":
            st.warning("Please enter some text.")
        else:
            # Classify the input text
            label = classify_text(input_text)

            # Display result in a table-like format
            result_df = pd.DataFrame({
                "Text": [input_text],
                "Label": [label]
            })
            st.write(result_df)

# Run the Streamlit app
if __name__ == "__main__":
    run()
