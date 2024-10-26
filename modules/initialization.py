# modules/initialization.py

import streamlit as st
from dotenv import load_dotenv
from modules.logger import setup_logging

def initialize_app():
    """Initializes the application by setting up environment variables, logging, and session state."""
    # Load environment variables
    load_dotenv()
    
    # Set up logging
    setup_logging()
    
    # Initialize session state variables
    if 'ai_response_text' not in st.session_state:
        st.session_state.ai_response_text = ''
    
    if 'previous_model' not in st.session_state:
        st.session_state.previous_model = None
        st.session_state.first_run = True
    else:
        st.session_state.first_run = False
