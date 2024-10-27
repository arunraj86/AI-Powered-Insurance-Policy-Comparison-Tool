# modules/csv_generator.py

import pandas as pd
import re

def create_csv_from_markdown(markdown_text):
    """
    Converts a markdown table to CSV format.

    Args:
        markdown_text (str): The markdown text containing the table.

    Returns:
        str: CSV formatted string.
    """
    # Extract the markdown table
    table_start = markdown_text.find('|')
    table_end = markdown_text.rfind('|')

    if table_start == -1 or table_end == -1:
        return ""  # No table found

    table_text = markdown_text[table_start:table_end + 1]
    lines = table_text.strip().split('\n')

    headers = [header.strip() for header in lines[0].split('|') if header.strip()]
    rows = []

    for line in lines[2:]:  # Skip header and separator
        columns = [col.strip() for col in line.split('|') if col.strip()]
        if columns:
            rows.append(columns)

    df = pd.DataFrame(rows, columns=headers)
    return df.to_csv(index=False)
