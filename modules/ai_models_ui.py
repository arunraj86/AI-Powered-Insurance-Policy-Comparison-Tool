import streamlit as st

def model_options():
    """Provides UI for AI model and insurance type selection."""

    st.sidebar.markdown(
        """
        <style>
        /* Change sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #f0f0f5;
        }
        /* Adjust the text color for sidebar headers */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
            color: #00796b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.title("AI Model Options")
    st.sidebar.markdown('<style>h1, h2, h3, h4 {color: #00796b;}</style>', unsafe_allow_html=True)

     # Select AI Model
    model_selection = st.sidebar.radio(
        "Select AI Model:",
        options=["Llama 3.1 70B", "OpenAI GPT-4"],
        index=0,
        help="Choose the type of AI model you want to use for comparison."
    )

    st.sidebar.title("Insurance Type Options")
    st.sidebar.markdown('<style>h1, h2, h3, h4 {color: #00796b;}</style>', unsafe_allow_html=True)
    # Select Insurance Type
    insurance_type = st.sidebar.radio(
        "Select Insurance Type:", 
        options=["Health", "Life", "Auto", "Homeowners or Renters", "Disability", "Travel", "Pet"], 
        help="Choose the type of insurance policies you are comparing."
    )

    return model_selection, insurance_type  # Make sure this line exists and returns both selections

    
