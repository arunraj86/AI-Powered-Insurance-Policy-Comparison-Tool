import streamlit as st

def model_options():
    """Provides UI for AI model selection."""
    st.sidebar.title("AI Model Options")
    st.sidebar.markdown('<style>h1, h2, h3, h4 {color: #00796b;}</style>', unsafe_allow_html=True)

    model_selection = st.sidebar.radio(
        "Select AI Model:",
        options=["Llama 3.1 70B", "OpenAI GPT-4"],
        index=0
    )

    return model_selection  # Return selected model
