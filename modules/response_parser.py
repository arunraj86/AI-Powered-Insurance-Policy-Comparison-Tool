# modules/response_parser.py

import pandas as pd
import streamlit as st
import re
import json
import logging

def parse_gpt_response(response_text):
    """Parse the GPT-4 response and extract the table and chart data."""
    # Extract the markdown table
    table_start = response_text.find('|')
    table_end = response_text.rfind('|')

    if table_start == -1 or table_end == -1:
        # No table found, return the raw text for GPT-4 responses
        return None, response_text, None

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

    # Extract JSON chart data
    chart_data = extract_json_from_markdown(response_text)

    return df, response_text, chart_data

def extract_json_from_markdown(markdown_text):
    """
    Extracts JSON object or list from the AI's markdown response.

    Args:
        markdown_text (str): The complete markdown text from AI.

    Returns:
        dict or list: Parsed JSON data.
    """
    # Regular expression to find JSON within markdown code block
    json_regex = r'```json\s*(\{.*?\}|\[.*?\])\s*```'
    match = re.search(json_regex, markdown_text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            st.error("Failed to decode JSON from AI response.")
            return {}
    else:
        logging.error("No JSON data found in AI response")
        #st.error("No JSON data found in AI response.")
        return {}
