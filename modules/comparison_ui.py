import streamlit as st

def comparison_form():
    """Renders the form to collect insurance policies for comparison."""
    st.markdown('<style>h1, h2, h3, h4 {color: #003366;}</style>', unsafe_allow_html=True)
    
    num_policies = st.number_input('Enter number of policies to compare:', min_value=2, max_value=10, step=1)
    
    policies = []
    columns = st.columns(2)  # Create two columns for input

    for i in range(num_policies):
        with columns[i % 2]:  # Alternate between the two columns
            st.subheader(f"Policy {i + 1}")
            provider = st.text_input(f"Provider Name (Policy {i + 1}):", key=f'provider_{i}')
            coverage = st.text_area(f"Coverage Details (Policy {i + 1}):", key=f'coverage_{i}')
            premium = st.number_input(f"Monthly Premium (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'premium_{i}')
            deductible = st.number_input(f"Deductible (Policy {i + 1}):", min_value=0.0, step=0.01, key=f'deductible_{i}')
            
            policy = {
                'provider': provider,
                'coverage': coverage,
                'premium': premium,
                'deductible': deductible
            }
            policies.append(policy)
    
    return policies
