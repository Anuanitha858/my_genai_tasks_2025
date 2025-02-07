import streamlit as st
st.set_page_config(page_title="Streamlit App", page_icon="💼", layout="wide")
from streamlit_option_menu import option_menu
import streamlit_app
import chatbot_single
import chatbot_multiple
import emailspamdetection
import summarization
import sentiment
import language  
import grammar
import text_classification

import content_generation 
# Apply Medium Pink Theme to Sidebar & Remove Scrollbar
st.markdown("""
    <style>
        /* Sidebar Background - Medium Pink */
        [data-testid="stSidebar"] {
            background-color: #D87093;  /* Medium Pink */
            padding: 20px;
            border-right: 2px solid #C71585; /* Deep Pink Border */
            overflow: hidden;  /* Removes scrollbar */
        }

        /* Sidebar Text - White */
        [data-testid="stSidebarNav"] {
            color: #ffffff;
            font-size: 18px;
            font-weight: bold;
        }

        /* Sidebar Links */
        [data-testid="stSidebar"] a {
            color: #ffffff !important;
            font-size: 16px;
        }

        /* Hover Effect for Sidebar Links - Light Pink */
        [data-testid="stSidebar"] a:hover {
            color: #FFB6C1 !important;  /* Light Pink */
            font-weight: bold;
        }

        /* Hide Sidebar Scrollbar */
        ::-webkit-scrollbar {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


# Sidebar with menu options
with st.sidebar:
    selected = option_menu(
        menu_title="Main menu",
        options=[
            "📜 Data extraction", 
            "💬 Invoice QnA", 
            "💬📄 Multiple Invoice QnA", 
            "📧 Email Spam Detection", 
            "📝 Summarization", 
            "🧠💬 Sentiment Analysis", 
            "🌍🈶 Language Detection", 
            "🔤 Grammar correction", 
            "✅ Text classification", 
            "📝 Content Generation"
        ],
        icons=[
            "home",     
            "home",                  
            "home",                   
            "home",               
            "home",       
            "home",                   
            "home",                   
            "home",              
            "home",            
            "home" ,
            "home"                     
        ]
    )

# Handling different menu options
if selected == "📜 Data extraction":
    streamlit_app.run()

elif selected == "💬 Invoice QnA":
    chatbot_single.run()

elif selected == "💬📄 Multiple Invoice QnA":
    chatbot_multiple.run()

elif selected == "📧 Email Spam Detection":
    emailspamdetection.run()

elif selected == "📝 Summarization":
    summarization.run()

elif selected == "🧠💬 Sentiment Analysis":
    sentiment.run()

elif selected == "🌍🈶 Language Detection":
    language.run()

elif selected == "🔤 Grammar correction":
    grammar.run()

elif selected == "✅ Text classification":
    text_classification.run()
 

elif selected == "📝 Content Generation":
    content_generation.run()     