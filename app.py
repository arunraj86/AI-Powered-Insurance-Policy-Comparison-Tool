# main_app.py

import streamlit as st
from modules.initialization import initialize_app
from modules.ui_components import (
    create_clear_buttons, 
    display_sidebar_help, 
    display_title,
)
from modules.comparison_ui import comparison_form
from modules.business_logic import handle_comparison
from modules.report_generation import generate_and_display_report
from modules.ai_models_ui import model_options

def main():
    # Initialize the application
    initialize_app()
        
    # Display the title
    display_title()
    
    # Sidebar for model and insurance type selection
    selected_model, selected_insurance_type = model_options()
    
    # Detect model change and reset report if necessary
    if not st.session_state.get('first_run', True):
        if st.session_state.get('previous_model') != selected_model:
            # Reset the comparison report
            st.session_state.ai_response_text = ''
            st.session_state.comparison_df = None
            st.session_state.chart_data = None
            st.session_state.previous_model = selected_model
            st.toast("AI model selection changed. Previous comparison report has been cleared.", icon="⚠️")
    else:
        # On first run, set the previous_model to the selected_model without showing a warning
        st.session_state.previous_model = selected_model
        st.session_state.first_run = False
    
    # Create clear buttons
    create_clear_buttons()
    
    # Render the comparison form
    policies = comparison_form(selected_insurance_type)
    
    # Handle the comparison logic
    handle_comparison(policies, selected_model, selected_insurance_type)
    
    # Generate and display report and chart
    generate_and_display_report()
    
    # Display sidebar help
    display_sidebar_help()

if __name__ == '__main__':
    main()
