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

# Sidebar content for branding and app info
with st.sidebar:
    st.title("💬 Jayaram's ChatBot")
    st.markdown(
        """
        Welcome to **Jayaram's ChatBot** powered by Gemini-Pro!
        - **AI Model**: Google Gemini-Pro
        - **Developer**: Jayaram
        """)

GOOGLE_API_KEY = 'AIzaSyBFil7kyMvheGHVhU5-YNTmQnLd_MJueXI'

if not GOOGLE_API_KEY:
    st.error("Google API key is missing. Please check your .env file.")
else:
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
        try:
            st.session_state.chat_session = model.start_chat(history=[])
        except Exception as e:
            st.error(f"Error starting chat session: {e}")

    # Display the chatbot's title on the page
    st.title("🤖 Jayaram's - ChatBot")

    # Display the chat history
    try:
        for message in st.session_state.chat_session.history:
            with st.chat_message(translate_role_for_streamlit(message.role)):
                st.markdown(message.parts[0].text)
    except Exception as e:
        st.error(f"Error displaying chat history: {e}")

    # Input field for user's message
    try:
        user_prompt = st.chat_input("Ask question...")
        if user_prompt:
            # Add user's message to chat and display it
            st.chat_message("user").markdown(user_prompt)

            # Send user's message to Gemini-Pro and get the response
            try:
                gemini_response = st.session_state.chat_session.send_message(user_prompt)
                # Display Gemini-Pro's response
                with st.chat_message("assistant"):
                    st.markdown(gemini_response.text)
            except Exception as e:
                st.error(f"Error getting response from Gemini-Pro: {e}")
    except Exception as e:
        st.error(f"Error with chat input: {e}")
