import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Jayaram!",
    page_icon="🧊",  # Favicon emoji
    layout="wide",   # Page layout option
    initial_sidebar_state="expanded",  # Sidebar is expanded by default
)

# Apply custom CSS for full black window styling
st.markdown(
    """
    <style>
    /* Full black background for the entire window */
    .stApp {
        background-color: black;
        color: white;
        font-family: "Segoe UI", sans-serif;
    }

    /* Chat bubble styling for user */
    .chat-user {
        background-color: #1e1e1e;  /* Dark gray for user chat bubble */
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        font-weight: bold;
        border: 2px solid #ffa726;
        width: 60%;  /* Adjust width for chat bubbles */
        word-wrap: break-word;
    }

    /* Chat bubble styling for assistant */
    .chat-assistant {
        background-color: #333333;  /* Slightly lighter dark gray for assistant chat bubble */
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #64b5f6;
        width: 60%;
        word-wrap: break-word;
    }

    /* Font customization */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        color: white;
    }

    .stTextInput label {
        font-size: 1.2em;
        font-weight: bold;
        color: white;
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: #1e1e1e;  /* Dark gray background for sidebar */
        padding: 20px;
        color: white;
    }

    /* Chat input field */
    .stTextInput input {
        background-color: #333333; /* Dark background for input */
        color: white;
        width: 100%; /* Ensure input takes full width */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content for branding and app info
with st.sidebar:
    st.title("💬 Jayaram's ChatBot")
    st.markdown(
        """
        Welcome to **Jayaram's ChatBot** powered by Gemini-Pro!
        - **AI Model**: Google Gemini-Pro
        - **Developer**: Jayaram
        """)
    

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 Jayaram's - ChatBot")

 # Display the chat history with enhanced styling
    for message in st.session_state.chat_session.history:
        role = translate_role_for_streamlit(message.role)
        chat_class = "chat-user" if role == "user" else "chat-assistant"
        st.markdown(
            f'<div class="{chat_class}">{message.parts[0].text}</div>',
            unsafe_allow_html=True
        )
#
    # Input field for user's message
    user_prompt = st.text_input("Ask Jayaram...")

    if user_prompt:
        # Add user's message to chat and display it
        st.markdown(f'<div class="chat-user">{user_prompt}</div>', unsafe_allow_html=True)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(f'<div class="chat-assistant">{gemini_response.text}</div>', unsafe_allow_html=True)

