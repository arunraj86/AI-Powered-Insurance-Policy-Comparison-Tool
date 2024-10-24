import streamlit as st

def model_options():
    """Provides UI for AI model and insurance type selection."""

    st.sidebar.markdown(
        """
        <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #333333; /* Dark background */
            color: #ffffff; /* White text */
        }

        /* Sidebar text color */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, 
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: #ffffff; /* White text for headers and labels */
        }

        /* Sidebar input field background color */
        [data-testid="stSidebar"] input {
            background-color: #444444; /* Slightly lighter background for input fields */
            color: #ffffff; /* White text */
        }

        /* Adjust scrollbar colors for better visibility */
        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-thumb {
            background: #888; 
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #555; 
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

    
