import streamlit as st

def comparison_form(insurance_type):
    """Renders the form to collect insurance policies for comparison."""
    st.markdown('<style>h1, h2, h3, h4 {color: #003366;}</style>', unsafe_allow_html=True)

    # Check if the insurance type has changed, and reset the form if it has
    if 'previous_insurance_type' not in st.session_state:
        st.session_state['previous_insurance_type'] = insurance_type

    # If the insurance type changes, reset the form
    if st.session_state['previous_insurance_type'] != insurance_type:
        reset_form()
        st.session_state['previous_insurance_type'] = insurance_type 

    # Add a reset button to manually clear inputs
    if st.button("Clear Data"):
        reset_form()
        
    # Number of policies input
    num_policies = st.number_input('Enter number of policies to compare:', min_value=2, max_value=10, step=1)

    policies = []
    columns = st.columns(2)  # Create two columns for input

    for i in range(num_policies):
        with columns[i % 2]:  # Alternate between the two columns
            st.subheader(f"Policy {i + 1}")
            provider = st.text_input(f"Provider Name (Policy {i + 1}):", key=f'provider_{i}')
            coverage = st.text_area(f"Coverage Details (Policy {i + 1}):", key=f'coverage_{i}')
            premium = st.number_input(f"Monthly Premium (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'premium_{i}')
            
            # Check if insurance type is Auto and adjust deductible inputs
            if insurance_type.lower() == "auto":
                collision_deductible = st.number_input(
                    f"Collision Deductible (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'collision_deductible_{i}'
                )
                comprehensive_deductible = st.number_input(
                    f"Comprehensive Deductible (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'comprehensive_deductible_{i}'
                )
                deductible = {
                    'collision': collision_deductible,
                    'comprehensive': comprehensive_deductible
                }
            else:
                deductible = st.number_input(f"Deductible (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'deductible_{i}')

            policy = {
                'provider': provider,
                'coverage': coverage,
                'premium': premium,
                'deductible': deductible
            }
            policies.append(policy)

    return policies

def reset_form():
    """Manually reset all session state form values."""
    for key in list(st.session_state.keys()):
        # Reset text fields to empty and numeric fields to 0.0
        if 'provider_' in key or 'coverage_' in key:
            st.session_state[key] = ''
        elif 'premium_' in key or 'deductible_' in key or 'collision_deductible_' in key or 'comprehensive_deductible_' in key:
            st.session_state[key] = 0.0
