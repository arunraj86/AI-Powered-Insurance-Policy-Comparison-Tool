# modules/messaging.py

import streamlit as st  # Import Streamlit
import time

def display_temp_message(message, msg_type="success", duration=3):
    """
    Displays a temporary message that disappears after a specified duration.
    
    Args:
        message (str): The message to display.
        msg_type (str): Type of message ('success', 'warning', 'error', 'info').
        duration (int): Duration in seconds before the message disappears.
    """
    placeholder = st.empty()
    if msg_type == "success":
        placeholder.success(message)
    elif msg_type == "warning":
        placeholder.warning(message)
    elif msg_type == "error":
        placeholder.error(message)
    elif msg_type == "info":
        placeholder.info(message)
    
    # Wait for the specified duration and then clear the message
    time.sleep(duration)
    placeholder.empty()
