from dotenv import load_dotenv
import logging
from modules.logger import setup_logging
from modules.comparison_ui import comparison_form
from modules.ai_models_ui import model_options
from modules.ai_api import compare_policies_with_model

# Set up logging
setup_logging()

# Load environment variables
load_dotenv()

def clean_response_text(response_text):
    """Clean the model's response text by removing unwanted newlines and spaces."""
    # Remove unnecessary newlines
    cleaned_text = response_text.replace("\n", " ").replace("  ", " ")
    return cleaned_text

def main():
    # Title and description
    st.title("AI-Powered Insurance Policy Comparison Tool")
    
    # Sidebar for model selection
    selected_model = model_options()

    # Display form for insurance policy comparison
    policies = comparison_form()

    # Comparison button logic
    if st.button("Compare Policies"):
        if all([p['provider'] and p['coverage'] for p in policies]):
            try:
                _, ai_response_text = compare_policies_with_model(policies, model=selected_model)
                
                if selected_model == "OpenAI GPT-4" and ai_response_text:
                    st.subheader("Full Comparison Report")
                    st.markdown(ai_response_text)

                elif ai_response_text:
                    st.subheader("Full Comparison Report")
                    st.markdown(ai_response_text)

            except Exception as e:
                logging.error(f"Error in comparison: {e}")
                st.error("An error occurred during comparison. Please check the logs for details.")
        else:
            st.error("Please fill out all fields for each policy.")

if __name__ == '__main__':
    import streamlit as st
    st.run()
