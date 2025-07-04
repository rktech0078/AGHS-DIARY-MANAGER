import streamlit as st
import os
from datetime import datetime
from utils.pdf_generator import generate_diary_pdf

# Page configuration
st.set_page_config(
    page_title="School Diary Manager",
    page_icon="assets/school_logo_right.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean and Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #f8f9fa;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    
    /* Professional Header */
    .professional-header {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #4f46e5;
    }
    
    .professional-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .professional-header p {
        margin: 0;
        font-size: 1rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Clean containers */
    .clean-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease;
    }
    
    .clean-container:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Section titles */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f3f4f6;
    }
    
    /* Form controls */
    .stSelectbox > div > div {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4f46e5;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        outline: none;
    }
    
    .stDateInput > div > div > input {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.2s ease;
    }
    
    .stDateInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    /* Subject areas */
    .subject-area {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .subject-area:hover {
        border-color: #4f46e5;
        background: #f8faff;
    }
    
    /* Professional buttons */
    .stButton > button {
        background: #4f46e5;
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .stButton > button:hover {
        background: #4338ca;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: #059669;
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: #047857;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(5, 150, 105, 0.4);
    }
    
    /* Alert messages */
    .alert-success {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #16a34a;
        color: #15803d;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid #dc2626;
        color: #dc2626;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f59e0b;
        color: #d97706;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .professional-footer {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: #6b7280;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .professional-header h1 {
            font-size: 1.8rem;
        }
        
        .clean-container {
            padding: 1.5rem;
        }
        
        .section-title {
            font-size: 1.1rem;
        }
        
        .stButton > button,
        .stDownloadButton > button {
            padding: 12px 24px;
            font-size: 0.9rem;
        }
    }
    
    /* Subtle animations */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Form labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stDateInput > label {
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background: white;
        border: 1px solid #e5e7eb;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Professional Header
    st.markdown("""
    <div class="professional-header">
        <h1>🏫 AL-GHAZALI HIGH SCHOOL</h1>
        <p>Daily Class Diary Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo setup notification
    if not os.path.exists('assets/school_logo.png'):
        st.markdown("""
        <div class="alert-warning">
            <strong>📷 Logo Setup:</strong> Place your school logo as <code>school_logo.png</code> in the <code>assets/</code> folder for professional PDFs.
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 Logo Setup Instructions"):
        st.markdown("""
        **Setup your school logos:**
        - **Main Logo**: Save as `assets/school_logo.png`
        - **Secondary Logo**: Save as `assets/school_logo_right.png` (optional)
        - **Recommended**: 200x200 pixels, PNG format
        """)
    
    # Create output directory
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Basic Information
    st.markdown('<div class="clean-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 Basic Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        diary_date = st.date_input(
            "Date",
            value=datetime.now().date(),
            help="Select diary date"
        )
        
        classes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        selected_class = st.selectbox(
            "Class",
            classes,
            help="Select class"
        )
    
    with col2:
        teacher_name = st.text_input(
            "Class Teacher",
            placeholder="Enter teacher name",
            help="Class teacher's name"
        )
        
        section = st.text_input(
            "Section",
            placeholder="e.g., A, B, C",
            help="Class section (optional)"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom Subjects
    st.markdown('<div class="clean-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Additional Subjects</div>', unsafe_allow_html=True)
    
    col1_custom, col2_custom = st.columns(2)
    with col1_custom:
        new_subject1 = st.text_input("Custom Subject 1", key="custom_subject1", placeholder="Enter subject name")
    
    with col2_custom:
        new_subject2 = st.text_input("Custom Subject 2", key="custom_subject2", placeholder="Enter subject name")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subjects
    st.markdown('<div class="clean-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 Subject Entries</div>', unsafe_allow_html=True)
    
    # Define subjects
    subjects = {
        "📝 English": "english",
        "📜 Urdu": "urdu",
        "📐 Mathematics": "math",
        "🔬 Science": "science",
        "🕌 Islamiat": "islamiat",
        "💻 Nardban": "nardban",
        "📖 Masharti Ulom": "masharti_ulom",
        "🕋 Rasool e Arabi": "rasool_e_arabi",
    }
    
    # Add custom subjects
    if new_subject1:
        subjects[f"🆕 {new_subject1}"] = new_subject1.lower()
    if new_subject2:
        subjects[f"🆕 {new_subject2}"] = new_subject2.lower()
    
    diary_entries = {}
    
    # Create subject entries in two columns
    col1, col2 = st.columns(2)
    
    subject_items = list(subjects.items())
    mid_point = len(subject_items) // 2
    
    with col1:
        for subject_display, subject_key in subject_items[:mid_point]:
            st.markdown(f'<div class="subject-area">', unsafe_allow_html=True)
            diary_entries[subject_key] = st.text_area(
                subject_display,
                placeholder=f"Enter homework/notes for {subject_display}...",
                height=100,
                key=f"subject_{subject_key}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        for subject_display, subject_key in subject_items[mid_point:]:
            st.markdown(f'<div class="subject-area">', unsafe_allow_html=True)
            diary_entries[subject_key] = st.text_area(
                subject_display,
                placeholder=f"Enter homework/notes for {subject_display}...",
                height=100,
                key=f"subject_{subject_key}"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Notes
    st.markdown('<div class="clean-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 Additional Notes</div>', unsafe_allow_html=True)
    
    additional_notes = st.text_area(
        "General Notes & Announcements",
        placeholder="Any additional notes, announcements, or important information...",
        height=80
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate PDF Button
    if st.button("📄 Generate PDF", use_container_width=True):
        # Validation
        if not any(diary_entries.values()) and not additional_notes:
            st.markdown("""
            <div class="alert-error">
                <strong>⚠️ Error:</strong> Please enter at least one subject entry or additional note.
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Prepare data
        diary_data = {
            'date': diary_date,
            'class': selected_class,
            'teacher': teacher_name,
            'section': section,
            'subjects': diary_entries,
            'additional_notes': additional_notes
        }
        
        try:
            # Generate PDF
            with st.spinner("Generating PDF..."):
                pdf_path = generate_diary_pdf(diary_data)
            
            # Success message
            st.markdown("""
            <div class="alert-success">
                <strong>✅ Success!</strong> Diary PDF generated successfully!
            </div>
            """, unsafe_allow_html=True)
            
            # Download button
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                
                filename = f"diary_class_{selected_class}_{diary_date.strftime('%Y_%m_%d')}.pdf"
                
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
            
        except Exception as e:
            st.markdown(f"""
            <div class="alert-error">
                <strong>❌ Error:</strong> {str(e)}
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="professional-footer">
        <p><strong>Al-Ghazali High School</strong> • Diary Management System</p>
        <p><small>IT Department • Version 1.0</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()