import os
import logging
from dotenv import load_dotenv
import openai
from groq import Groq
import pandas as pd
import streamlit as st

load_dotenv()

# Load the API keys from environment variables
#groq_api_key = os.getenv("GROQ_API_KEY", "")
#openai_api_key = os.getenv("OPENAI_API_KEY", "")
# Accessing the keys from Streamlit secrets
groq_api_key = st.secrets["GROQ_API_KEY"]
openai_api_key = st.secrets["OPENAI_API_KEY"]

if not groq_api_key:
    raise ValueError("GROQ API key not found! Please set the 'GROQ_API_KEY' environment variable.")

if not openai_api_key:
    raise ValueError("OpenAI API key not found! Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize the clients
groq_client = Groq(api_key=groq_api_key)
openai.api_key = openai_api_key

def create_policy_comparison_prompt(policies):
    """Create a structured prompt to compare insurance policies with markdown table format."""
    prompt = (
        "You are a financial expert. Please compare the following insurance policies in detail. "
        "Your response should include:\n"
        "1. A **Comparison Report** in the form of a markdown table. The table should have the following columns: "
        "`Provider Name`, `Coverage Details`, `Monthly Premium`, and `Deductibles`.\n"
        "2. A **Summary of Key Differences**: After the table, provide a brief summary highlighting the key differences between the policies, "
        "focusing on areas such as significant variations in coverage, affordability, premiums, or deductibles.\n"
        "3. **Recommendations**: Indicate which policy is better and why, considering factors like affordability, coverage, and benefits.\n"
        "4. **Explanations**: For each policy, provide an introductory paragraph summarizing the overall strengths and weaknesses of the policy, "
        "and then format the pros and cons in bullet points as follows:\n"
        "- **Pros**:\n"
        "  - List the benefits of the policy, such as lower premiums, higher coverage, or better terms.\n"
        "- **Cons**:\n"
        "  - List the downsides of the policy, such as higher premiums, lower coverage, or less favorable terms.\n\n"
        "Please format the comparison as a table using the following format:\n"
        "| Provider Name | Coverage Details | Monthly Premium | Deductibles |\n"
        "| ------------- | ---------------- | --------------- | ----------- |\n"
    )

    # Adding each policy's details in a row format in the markdown table
    for idx, policy in enumerate(policies):
        prompt += f"| {policy['provider']} | {policy['coverage']} | {policy['premium']} | {policy['deductible']} |\n"

    # Return the final prompt string with the markdown table
    return prompt


def parse_gpt_response(response_text):
    """Parse the GPT-4 response and extract the table for comparison."""
    # Find the markdown table in the response (specific for GPT-4 model)
    table_start = response_text.find('|')
    table_end = response_text.rfind('|')

    if table_start == -1 or table_end == -1:
        # No table found, return the raw text for GPT-4 responses
        return None, response_text

    # Extract the table portion
    table_text = response_text[table_start:table_end + 1]

    # Split lines and remove markdown syntax
    lines = table_text.strip().split('\n')
    
    headers = [col.strip() for col in lines[0].split('|') if col.strip()]
    rows = []
    
    for line in lines[2:]:
        cols = [col.strip() for col in line.split('|') if col.strip()]
        if cols:
            rows.append(cols)

    # Create DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df, response_text

def compare_policies_with_model(policies, model="Llama 3.1 70B"):
    """Generate a comparison report using the selected AI model."""
    prompt = create_policy_comparison_prompt(policies)

    try:
        if model == "Llama 3.1 70B":
            # Call the Llama API for Llama
            response = groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            if response.choices and len(response.choices) > 0:
                # Return the plain Llama response without attempting to parse it
                return None, response.choices[0].message.content  # Return Llama response text only
        
        elif model == "OpenAI GPT-4":
            # Call the OpenAI API for GPT-4
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            if response.choices and len(response.choices) > 0:
                # Get the content from the GPT response
                response_text = response.choices[0].message.content
                
                # Parse the GPT response text into a table and return both the table and the text
                comparison_table, full_text = parse_gpt_response(response_text)
                
                return comparison_table, full_text

        else:
            return None, "Unsupported AI model selected."

    except Exception as e:
        logging.error(f"Error during AI model inference: {e}")
        raise e
