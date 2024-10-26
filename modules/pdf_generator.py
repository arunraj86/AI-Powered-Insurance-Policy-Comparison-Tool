# modules/pdf_generator.py

from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import markdown
from bs4 import BeautifulSoup

def create_pdf_from_markdown_reportlab(markdown_text):
    """
    Convert Markdown text to PDF bytes using ReportLab.

    Parameters:
        markdown_text (str): The Markdown formatted text containing tables and sections.

    Returns:
        bytes: The generated PDF in bytes.
    """
    # Initialize a buffer to hold PDF data
    buffer = BytesIO()
    
    # Create a SimpleDocTemplate
    doc = SimpleDocTemplate(buffer, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Modify existing 'Heading1' style
    heading1_style = styles['Heading1']
    heading1_style.fontSize = 18
    heading1_style.leading = 22
    heading1_style.spaceAfter = 12
    
    # Modify existing 'Heading2' style
    heading2_style = styles['Heading2']
    heading2_style.fontSize = 16
    heading2_style.leading = 20
    heading2_style.spaceAfter = 10
    
    # Add a custom style if needed
    styles.add(ParagraphStyle(
        name='BodyTextCustom',
        parent=styles['BodyText'],
        fontSize=12,
        leading=14,
        spaceAfter=12
    ))
    
    # Split Markdown into lines
    lines = markdown_text.split('\n')
    
    # Initialize Story list
    Story = []
    
    # Temporary storage for table lines
    table_lines = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            # Empty line, add space
            Story.append(Spacer(1, 12))
            continue
        
        if line.startswith("**") and line.endswith("**"):
            # Bold text, treat as Heading
            heading_text = line.strip("*").strip()
            Story.append(Paragraph(heading_text, heading2_style))
            Story.append(Spacer(1, 12))
        
        elif line.startswith("### "):
            # Sub-heading
            sub_heading = line.replace("### ", "").strip()
            Story.append(Paragraph(sub_heading, heading2_style))
            Story.append(Spacer(1, 12))
        
        elif line.startswith("|"):
            # Table row
            table_lines.append(line)
        
        elif line.startswith("* "):
            # Bullet point
            bullet_text = line.replace("* ", "• ", 1).strip()
            Story.append(Paragraph(bullet_text, styles['BodyTextCustom']))
            Story.append(Spacer(1, 6))
        
        else:
            # Regular text
            Story.append(Paragraph(line, styles['BodyTextCustom']))
            Story.append(Spacer(1, 12))
    
    # After processing all lines, handle any remaining table
    if table_lines:
        table_data = []
        for tbl_line in table_lines:
            # Remove leading and trailing '|', then split by '|'
            row = [cell.strip() for cell in tbl_line.strip("|").split("|")]
            table_data.append(row)
        
        # Create Table
        tbl = Table(table_data, hAlign='LEFT')
        
        # Add style to the table
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        
        Story.append(tbl)
        Story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(Story)
    
    # Get PDF data
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

