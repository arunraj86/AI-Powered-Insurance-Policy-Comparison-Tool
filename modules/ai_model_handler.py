import os
import logging
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
from modules.prompt_generator import create_policy_comparison_prompt
from modules.response_parser import parse_gpt_response

load_dotenv()

# Load the API keys from environment variables
#groq_api_key = os.getenv("GROQ_API_KEY", "")
#openai_api_key = os.getenv("OPENAI_API_KEY", "")
# Accessing the keys from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

if not groq_api_key:
    raise ValueError("GROQ API key not found! Please set the 'GROQ_API_KEY' environment variable.")

if not openai_api_key:
    raise ValueError("OpenAI API key not found! Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize the clients
groq_client = Groq(api_key=groq_api_key)
client = OpenAI(api_key=openai_api_key)

def compare_policies_with_model(policies, model="Llama 3.1 70B",insurance_type="Auto"):
    """Generate a comparison report using the selected AI model."""
    prompt = create_policy_comparison_prompt(policies,insurance_type)

    try:
        if model == "Llama 3.1 70B":
            # Call the Llama API for Llama
            response = groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            if response.choices and len(response.choices) > 0:
                # Return the plain Llama response without attempting to parse it
                return None, response.choices[0].message.content  # Return Llama response text only

        elif model == "OpenAI GPT-4":
            # Use the Chat API for GPT-4
            response = client.chat.completions.create(
                model="gpt-4",  # Specify the chat model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},  # System message defining the assistant's role
                    {"role": "user", "content": prompt}  # User's prompt (e.g., the insurance policies comparison request)
                ],
                max_tokens=1500,  # Maximum tokens in the response
                temperature=0.7  # Controls the creativity or randomness of the response)
            )
            if response.choices and len(response.choices) > 0:
                # Get the content from the GPT response
                response_text = response.choices[0].message.content

                # Parse the GPT response text into a table and return both the table and the text
                comparison_table, full_text = parse_gpt_response(response_text)

                return comparison_table, full_text

        else:
            return None, "Unsupported AI model selected."

    except Exception as e:
        logging.error(f"Error during AI model inference: {e}")
        st.error(f"An error occurred during AI model inference: {e}")  # Display the error in Streamlit UI
        raise e
