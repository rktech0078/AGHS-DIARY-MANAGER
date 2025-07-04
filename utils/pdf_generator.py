from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime
from reportlab.platypus import KeepInFrame




def generate_diary_pdf(diary_data):
    """
    Generate a professional diary PDF with proper table formatting and dual logos
    """
    
    # Create filename
    date_str = diary_data['date'].strftime('%Y_%m_%d')
    class_name = diary_data['class'].replace(' ', '_')
    filename = f"diary_{class_name}_{date_str}.pdf"
    filepath = os.path.join('output', filename)
    
    # Create PDF document with custom margins for header space
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=140,  # Increased for header with logos
        bottomMargin=80
    )
    
    # Container for PDF elements
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'SchoolTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1a365d'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        letterSpacing=1
    )
    
    subtitle_style = ParagraphStyle(
        'DiarySubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2d3748'),
        alignment=TA_CENTER,
        spaceAfter=25,
        fontName='Helvetica-Bold'
    )
    
    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#2b6cb0'),
        borderPadding=8
    )
    
    # Helper function to clean text for PDF compatibility
    def clean_text(text):
        if not text:
            return ""
        # Replace problematic Unicode characters
        text = str(text)
        text = text.replace('-', '-')  # En dash to hyphen
        text = text.replace('—', '-')  # Em dash to hyphen
        text = text.replace(''', "'")  # Smart quote
        text = text.replace(''', "'")  # Smart quote
        text = text.replace('"', '"')  # Smart quote
        text = text.replace('"', '"')  # Smart quote
        # Remove any other non-ASCII characters
        text = ''.join(char if ord(char) < 128 else '?' for char in text)
        return text
    
    # Basic Information Section (as a clean table)
    date_formatted = diary_data['date'].strftime('%A, %B %d, %Y')
    class_info = clean_text(diary_data['class'])
    if diary_data.get('section'):
        class_info += f" - Section {clean_text(diary_data['section'])}"
    
    # Create info table
    info_data = [
        ['Date:', date_formatted, 'Level:', class_info],
    ]
    
    if diary_data.get('teacher'):
        info_data.append(['Teacher:', clean_text(diary_data['teacher']), '', ''])
    
    info_table = Table(info_data, colWidths=[1*inch, 2.2*inch, 1*inch, 2.2*inch])
    info_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2d3748')),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#2d3748')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 25))
    
    # Subject Entries Section Header
    story.append(Paragraph("SUBJECT-WISE DIARY ENTRIES", section_header_style))
    story.append(Spacer(1, 15))
    
    # Subject mapping for better display
    subject_mapping = {
        'english': 'English & WorkBook',
        'urdu': 'Urdu', 
        'math': 'Mathematics',
        'science': 'Science',
        'islamiat': 'Islamic Studies',
        'nardban': 'Nardban',
        'masharti_ulom': 'Masharti Ulom',
        'rasool_e_arabi': 'Rasool e Arabi',
    }
    
    # Create subjects table
    subject_data = [['Subject', 'Homework / Notes']]  # Header row
    
    # Add subjects with content
    has_content = False
    for subject_key, content in diary_data['subjects'].items():
        if content and content.strip():
            has_content = True
            subject_name = subject_mapping.get(subject_key, subject_key.title())
            # Format content properly for table cell and clean it
            formatted_content = clean_text(content.strip())
            subject_data.append([subject_name, formatted_content])
    
    # Add empty subjects if no content
    if not has_content:
        subject_data.append(['No entries', 'No homework assigned for today'])
    
    # Create the subjects table
    subjects_table = Table(subject_data, colWidths=[2*inch, 4.5*inch])
    subjects_table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows styling
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2d3748')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Subject names bold
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),       # Content normal
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Grid and borders
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2b6cb0')),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')])
    ]))
    
    story.append(subjects_table)
    story.append(Spacer(1, 25))
    
    # Additional Notes Section
    if diary_data.get('additional_notes') and diary_data['additional_notes'].strip():
        story.append(Paragraph("ADDITIONAL NOTES & ANNOUNCEMENTS", section_header_style))
        story.append(Spacer(1, 15))
        
        # Create notes table
        notes_data = [
            ['Additional Information', clean_text(diary_data['additional_notes'].strip())]
        ]
        
        notes_table = Table(notes_data, colWidths=[2*inch, 4.5*inch])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#38a169')),
            ('BACKGROUND', (1, 0), (1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#2d3748')),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(notes_table)
    
    # Build PDF with custom page template
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    
    return filepath

def create_header_footer(canvas, doc):
    """
    Create professional header with dual logos and footer
    """
    # Page dimensions
    width, height = A4
    
    # Header section
    canvas.saveState()
    
    # Header background
    canvas.setFillColor(colors.HexColor('#f7fafc'))
    canvas.rect(0, height - 130, width, 130, fill=1, stroke=0)
    
    # Header border
    canvas.setStrokeColor(colors.HexColor('#2b6cb0'))
    canvas.setLineWidth(3)
    canvas.line(0, height - 130, width, height - 130)
    
    # Logo positions
    left_logo_path = 'assets/school_logo.png'
    right_logo_path = 'assets/school_logo_right.png'  # You can use same logo or different

    
    # Left logo
    if os.path.exists(left_logo_path):
        try:
            canvas.drawImage(left_logo_path, 60, height - 100, width=80, height=80, 
                           preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Could not load left logo: {e}")
    
    # Right logo (use same logo if right logo doesn't exist)
    right_logo = right_logo_path if os.path.exists(right_logo_path) else left_logo_path
    if os.path.exists(right_logo):
        try:
            canvas.drawImage(right_logo, width - 140, height - 100, width=80, height=80, 
                           preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Could not load right logo: {e}")
    
    # School name and title
    canvas.setFillColor(colors.HexColor('#1a365d'))
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawCentredString(width/2, height - 60, "AL-GHAZALI HIGH SCHOOL")
    
    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(colors.HexColor('#2d3748'))
    canvas.drawCentredString(width/2, height - 85, "Daily Class Diary")
    
    # Decorative line under header
    canvas.setStrokeColor(colors.HexColor('#2b6cb0'))
    canvas.setLineWidth(2)
    # canvas.line(50, height - 140, width - 50, height - 140)
    
    
    # Footer section
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor('#718096'))
    
    # Generation info
    try:
        import pytz
        pk_tz = pytz.timezone('Asia/Karachi')
        current_time = datetime.now(pk_tz)
        generation_time = current_time.strftime('%B %d, %Y at %I:%M %p PKT')
    except:
        generation_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    canvas.drawCentredString(width/2, 50, "Generated by IT Department - Al-Ghazali High School")
    canvas.drawCentredString(width/2, 35, f"Created on {generation_time}")
    
    # Page number
    page_num = canvas.getPageNumber()
    canvas.drawRightString(width - 60, 35, f"Page {page_num}")
    
    # Footer line
    canvas.setStrokeColor(colors.HexColor('#e2e8f0'))
    canvas.setLineWidth(1)
    canvas.line(50, 25, width - 50, 25)
    
    canvas.restoreState()