# modules/csv_generator.py

import pandas as pd
import markdown
from bs4 import BeautifulSoup
import logging

def create_csv_from_markdown(markdown_text):
    """
    Convert Markdown text to CSV format by extracting tables.

    Parameters:
        markdown_text (str): The Markdown formatted text containing tables.

    Returns:
        str: A single CSV string combining all extracted tables with headers.
    """
    logging.info("Starting CSV generation from Markdown.")

    # Convert Markdown to HTML with table extension
    try:
        html = markdown.markdown(markdown_text, extensions=['tables'])
        logging.debug("Converted Markdown to HTML.")
    except Exception as e:
        logging.error(f"Failed to convert Markdown to HTML: {e}")
        return ""

    # Parse HTML content
    try:
        soup = BeautifulSoup(html, "html.parser")
        logging.debug("Parsed HTML content with BeautifulSoup.")
    except Exception as e:
        logging.error(f"Failed to parse HTML with BeautifulSoup: {e}")
        return ""

    # Find all tables in the HTML
    tables = soup.find_all("table")
    logging.info(f"Found {len(tables)} table(s) in the Markdown.")

    if not tables:
        logging.warning("No tables found in the provided Markdown text.")
        return ""

    # Initialize a list to hold CSV strings
    csv_list = []

    for idx, table in enumerate(tables, start=1):
        try:
            # Use pandas to read the HTML table
            df = pd.read_html(str(table))[0]
            logging.debug(f"Extracted Table_{idx} with shape {df.shape}.")

            # Replace any newline characters in the data to prevent CSV format issues
            df = df.replace('\n', ' ', regex=True)

            # Convert DataFrame to CSV string
            csv_string = df.to_csv(index=False)

            # Add a header to identify the table
            csv_list.append(f"Table_{idx}\n{csv_string}\n")
            logging.debug(f"Converted Table_{idx} to CSV format.")
        except Exception as e:
            logging.error(f"Failed to process Table_{idx}: {e}")

    # Combine all tables into a single CSV string
    combined_csv = "\n".join(csv_list)
    logging.info("Completed CSV generation from Markdown.")

    return combined_csv
