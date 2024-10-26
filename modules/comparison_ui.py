# modules/comparison_ui.py

import streamlit as st  # Import Streamlit
from modules.utilities import reset_form  # Import reset_form from utilities.py
from modules.messaging import display_temp_message  # Import messaging function if needed

def comparison_form(insurance_type):
    """Renders the form to collect insurance policies for comparison with validation."""
    st.markdown('<style>h1, h2, h3, h4 {color: #003366;}</style>', unsafe_allow_html=True)

    # Check if the insurance type has changed, and reset the form if it has
    if 'previous_insurance_type' not in st.session_state:
        st.session_state['previous_insurance_type'] = insurance_type

    # If the insurance type changes, reset the form and clear the comparison report
    if st.session_state['previous_insurance_type'] != insurance_type:
        reset_form()
        st.session_state.ai_response_text = ''  # Clear the comparison report
        st.toast("Insurance type changed. Previous comparison report has been cleared.", icon="⚠️")
        st.session_state['previous_insurance_type'] = insurance_type 

    # Number of policies input
    num_policies = st.number_input(
        'Enter number of policies to compare:', 
        min_value=2, 
        max_value=10, 
        step=1, 
        key='num_policies'
    )

    policies = []
    columns = st.columns(2)  # Create two columns for input

    for i in range(int(num_policies)):
        with columns[i % 2]:  # Alternate between the two columns
            st.subheader(f"Policy {i + 1}")
            provider = st.text_input(f"Provider Name (Policy {i + 1}):", key=f'provider_{i}')
            coverage = st.text_area(f"Coverage Details (Policy {i + 1}):", key=f'coverage_{i}')
            premium = st.number_input(f"Monthly Premium (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'premium_{i}')
            
            # Check if insurance type is Auto and adjust deductible inputs
            if insurance_type.lower() == "auto":
                collision_deductible = st.number_input(
                    f"Collision Deductible (Policy {i + 1}):", 
                    min_value=0.0, 
                    step=0.01, 
                    key=f'collision_deductible_{i}'
                )
                comprehensive_deductible = st.number_input(
                    f"Comprehensive Deductible (Policy {i + 1}):", 
                    min_value=0.0, 
                    step=0.01, 
                    key=f'comprehensive_deductible_{i}'
                )
                deductible = {
                    'collision': collision_deductible,
                    'comprehensive': comprehensive_deductible
                }
            else:
                deductible = st.number_input(
                    f"Deductible (Policy {i + 1}):", 
                    min_value=0.0, 
                    step=0.01, 
                    key=f'deductible_{i}'
                )

            policy = {
                'provider': provider.strip(),
                'coverage': coverage.strip(),
                'premium': premium,
                'deductible': deductible
            }
            policies.append(policy)

    # Validation Logic
    validation_passed = True
    error_messages = []

    for idx, policy in enumerate(policies):
        if not policy['provider']:
            validation_passed = False
            error_messages.append(f"Provider Name for Policy {idx + 1} is required.")
        
        if not policy['coverage']:
            validation_passed = False
            error_messages.append(f"Coverage Details for Policy {idx + 1} are required.")
        
        if policy['premium'] <= 0:
            validation_passed = False
            error_messages.append(f"Monthly Premium for Policy {idx + 1} must be greater than 0.")
        
        if insurance_type.lower() == "auto":
            if policy['deductible']['collision'] < 0:
                validation_passed = False
                error_messages.append(f"Collision Deductible for Policy {idx + 1} cannot be negative.")
            if policy['deductible']['comprehensive'] < 0:
                validation_passed = False
                error_messages.append(f"Comprehensive Deductible for Policy {idx + 1} cannot be negative.")
        else:
            if policy['deductible'] < 0:
                validation_passed = False
                error_messages.append(f"Deductible for Policy {idx + 1} cannot be negative.")

    if not validation_passed:
        for message in error_messages:
            st.error(message)
        return []  # Return empty list if validation fails

    return policies
