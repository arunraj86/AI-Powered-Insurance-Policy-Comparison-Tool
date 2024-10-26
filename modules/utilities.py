# modules/utilities.py

import streamlit as st  # Import Streamlit
from modules.messaging import display_temp_message

def reset_form(clear_report=False):
    """Manually reset all session state form values.
    
    Args:
        clear_report (bool): Whether to also clear the comparison report.
    """
    keys_to_reset = [
        key for key in st.session_state.keys()
        if any(sub in key for sub in ['provider_', 'coverage_', 'premium_', 'deductible_', 'collision_deductible_', 'comprehensive_deductible_'])
    ]
    for key in keys_to_reset:
        st.session_state[key] = '' if 'provider_' in key or 'coverage_' in key else 0.0
    
    if clear_report:
        st.session_state.ai_response_text = ''
        display_temp_message("Form and comparison report have been reset.", "success", duration=2)
    else:
        display_temp_message("Form has been reset.", "success", duration=3)
