# modules/report_generation.py

import streamlit as st
from datetime import datetime
from modules.csv_generator import create_csv_from_markdown
from modules.pdf_generator import create_pdf_from_markdown_reportlab
from modules.messaging import display_temp_message
from modules.chart_generator import (
    create_premium_chart, 
    create_coverage_limit_chart, 
    create_deductibles_chart
)
import re
import json

def generate_and_display_report():
    """Generates CSV and PDF reports from the AI response and provides download buttons."""
    if st.session_state.get('ai_response_text'):
        # Retrieve the full AI response and chart data from session state
        response_text = st.session_state.ai_response_text
        chart_data = st.session_state.get('chart_data')

        # Initialize variables
        markdown_text = response_text  # Default to full response
        extracted_json = None

        # Attempt to extract JSON data enclosed within ```json code blocks
        json_code_block_pattern = r'```json\s*(\{.*?\}|\[.*?\])\s*```'
        json_match = re.search(json_code_block_pattern, response_text, re.DOTALL)

        if json_match:
            # Extract the JSON string
            json_str = json_match.group(1)
            try:
                # Parse the JSON string
                extracted_json = json.loads(json_str)
                # Update session state with the extracted JSON data
                st.session_state.chart_data = extracted_json
                # Remove the JSON block from the markdown text
                markdown_text = response_text.replace(json_match.group(0), '').strip()
            except json.JSONDecodeError:
                st.error("Failed to decode JSON from AI response.")
        else:
            # If no ```json code block is found, attempt to extract JSON array directly
            json_array_pattern = r'\[\s*\{.*?\}\s*\]'
            json_array_match = re.search(json_array_pattern, response_text, re.DOTALL)
            if json_array_match:
                json_str = json_array_match.group(0)
                try:
                    extracted_json = json.loads(json_str)
                    st.session_state.chart_data = extracted_json
                    markdown_text = response_text.replace(json_str, '').strip()
                except json.JSONDecodeError:
                    st.error("Failed to decode JSON from AI response.")
            else:
                st.warning("No JSON chart data found in the AI response.")
        
        # Display the markdown report without the JSON data
        st.subheader("Full Comparison Report")
        st.markdown(markdown_text)  # This will exclude the JSON block

        # Generate current timestamp for dynamic file names
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create CSV file from the markdown table
        csv_content = create_csv_from_markdown(markdown_text)
        
        # Dynamic file name for CSV
        csv_filename = f"comparison_report_{now}.csv"

        # Download button for CSV file
        if csv_content:
            st.download_button(
                label="Download Comparison Report as CSV",
                data=csv_content.encode('utf-8'),  # Encode to bytes
                file_name=csv_filename,
                mime="text/csv"
            )

        # Create PDF file from the markdown report using ReportLab
        try:
            pdf_bytes = create_pdf_from_markdown_reportlab(markdown_text)
            
            # Dynamic file name for PDF
            pdf_filename = f"comparison_report_{now}.pdf"
            
            # Download button for PDF file
            st.download_button(
                label="Download Comparison Report as PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Failed to generate PDF with ReportLab: {e}")

        # Generate and display the charts
        if extracted_json:
            # Monthly Premium Chart
            st.subheader("Comparison Chart: Monthly Premium")
            fig_premium = create_premium_chart(extracted_json)
            if fig_premium:
                st.plotly_chart(fig_premium, use_container_width=True)
            else:
                st.error("Failed to generate the Monthly Premium chart.")

            # Coverage Limit Chart
            st.subheader("Comparison Chart: Coverage Limit")
            fig_coverage = create_coverage_limit_chart(extracted_json)
            if fig_coverage:
                st.plotly_chart(fig_coverage, use_container_width=True)
            else:
                st.error("Failed to generate the Coverage Limit chart.")

            # Deductibles Chart
            st.subheader("Comparison Chart: Deductibles")
            fig_deductibles = create_deductibles_chart(extracted_json)
            if fig_deductibles:
                st.plotly_chart(fig_deductibles, use_container_width=True)
            else:
                st.error("Failed to generate the Deductibles chart.")
        else:
            st.warning("No chart data available to display.")
