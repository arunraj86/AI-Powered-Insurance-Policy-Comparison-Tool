# modules/report_generation.py

import streamlit as st  # Import Streamlit
from datetime import datetime
from modules.csv_generator import create_csv_from_markdown
from modules.pdf_generator import create_pdf_from_markdown_reportlab
from modules.messaging import display_temp_message

def generate_and_display_report():
    """Generates CSV and PDF reports from the AI response and provides download buttons."""
    if st.session_state.ai_response_text:
        st.subheader("Full Comparison Report")
        st.markdown(st.session_state.ai_response_text)  # Display the response text

        # Display the raw Markdown content for verification
        #st.markdown("### Raw Markdown Content")
        #st.code(st.session_state.ai_response_text, language='markdown')

        # Generate current timestamp for dynamic file names
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create CSV file from the response text
        csv_content = create_csv_from_markdown(st.session_state.ai_response_text)
        
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

        # Create PDF file from the response text using ReportLab
        try:
            pdf_bytes = create_pdf_from_markdown_reportlab(st.session_state.ai_response_text)
            
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
