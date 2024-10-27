# modules/ui_components.py

import streamlit as st  # Import Streamlit
from modules.utilities import reset_form
from modules.messaging import display_temp_message

def set_custom_button_styles():
    st.markdown(
        """
        <style>
        /* Universal button styling to ensure consistency */
        .stButton > button {
            background-color: #3CB371 !important; /* Custom green color */
            color: white !important;
            font-size: 18px !important;
            height: 2.5em !important;
            width: 18em !important;
            border-radius: 8px !important;
            border: none !important; /* Remove border if desired */
            cursor: pointer !important; /* Change cursor to pointer on hover */
            transition: background-color 0.3s ease; /* Smooth transition */
        }

        /* Hover effect for all buttons */
        .stButton > button:hover {
            background-color: #2E8B57 !important; /* Darker green on hover */
        }

        /* Specific button styling based on aria-label (optional) */
        /*
        button[aria-label="Clear Comparison Report"] {
            /* Add specific styles if needed */
        }

        button[aria-label="Clear Input Data"] {
            /* Add specific styles if needed */
        }

        button[aria-label="Compare Policies"] {
            /* Add specific styles if needed */
        }
        */
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom styles
set_custom_button_styles()

def create_clear_buttons():
    """Creates 'Clear Comparison Report' and 'Clear Input Data' buttons side by side."""
    clear_cols = st.columns(2)
    with clear_cols[0]:
        if st.button("Clear Comparison Report", key="clear_report_main"):
            st.session_state.ai_response_text = ''
            st.toast("Comparison report has been cleared.", icon="✅")
    with clear_cols[1]:
        if st.button("Clear Input Data", key="clear_data_main"):
            reset_form()
            st.toast("Form data has been cleared.", icon="✅")

def display_sidebar_help():
    """Displays the help instructions in the sidebar as a collapsible section."""
    with st.sidebar.expander("How to Use", expanded=False):
        st.markdown("""
        1. **Select AI Model:** Choose the AI model you'd like to use for generating the comparison report.
        2. **Select Insurance Type:** Choose the type of insurance policy you're comparing.
        3. **Input Policy Data:** Fill out the comparison form with details of each insurance policy.
        4. **Generate Report:** Click the "Compare Policies" button to generate the report.
        5. **Download Report:** Once generated, download the report as CSV or PDF using the provided buttons.
        6. **Clear Report & Data:** Use the "Clear Comparison Report" button to remove the generated report and the "Clear Input Data" button to reset the form inputs.
        """)

def display_title():
    """Displays the main title of the application."""
    st.title("AI-Powered Insurance Policy Comparison Tool")
