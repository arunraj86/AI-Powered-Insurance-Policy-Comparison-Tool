import pandas as pd

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