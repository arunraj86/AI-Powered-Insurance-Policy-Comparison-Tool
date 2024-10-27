# modules/business_logic.py

import streamlit as st
import logging
from modules.ai_model_handler import compare_policies_with_model
from modules.messaging import display_temp_message

def handle_comparison(policies, selected_model, selected_insurance_type):
    """Handles the comparison of policies using the selected AI model."""
    if st.button("Compare Policies", key="compare_policies"):
        if all([p['provider'] and p['coverage'] for p in policies]):
            with st.spinner('Generating comparison report...'):
                try:
                    df, ai_response_text, chart_data = compare_policies_with_model(
                        policies, 
                        model=selected_model, 
                        insurance_type=selected_insurance_type
                    )
                    
                    if ai_response_text:
                        # Store the response in session state
                        st.session_state.ai_response_text = ai_response_text
                        st.session_state.comparison_df = df
                        st.session_state.chart_data = chart_data
                        
                        display_temp_message("Comparison report generated successfully!", "success", duration=3)
                except Exception as e:
                    logging.error(f"Error in comparison: {e}")
                    display_temp_message("An error occurred during comparison. Please check the logs for details.", "error", duration=3)
        else:
            display_temp_message("Please fill out all fields for each policy.", "error", duration=3)
