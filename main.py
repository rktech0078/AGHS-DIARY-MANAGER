import streamlit as st
import os
from datetime import datetime
from utils.pdf_generator import generate_diary_pdf

# Page configuration
st.set_page_config(
    page_title="School Diary Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .form-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
    }
    
    .subject-input {
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 5px;
        font-weight: 600;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            font-size: 1.5rem;
        }
        .stButton {
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 AL-GHAZALI HIGH SCHOOL</h1>
        <p>Diary Manager - Daily Class Diary System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo information
    if not os.path.exists('assets/school_logo.png'):
        st.warning("📷 **Logo Setup**: Place your school logo as `school_logo.png` in the `assets/` folder for professional PDFs!")
    
    with st.expander("ℹ️ Logo Setup Instructions"):
        st.markdown("""
        **For best results, add your school logos:**
        - **Left Logo**: Save as `assets/school_logo.png`
        - **Right Logo**: Save as `assets/school_logo_right.png` (optional, will use left logo if not provided)
        - **Recommended size**: 200x200 pixels, PNG format with transparent background
        - **Best results**: Square logos with good contrast
        """)
    
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Main form container
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Form inputs
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📅 Basic Information")
            
            # Date input
            diary_date = st.date_input(
                "Select Date",
                value=datetime.now().date(),
                help="Choose the date for the diary",
            )
            
            # Class selection
            classes = [
                "1", "2", "3", "4", "5"
            ]
            
            selected_class = st.selectbox(
                "Select Class",
                classes,
                help="Choose the class for this diary"
            )
        
        with col2:
            st.subheader("👨‍🏫 Additional Details")
            
            # Class teacher name
            teacher_name = st.text_input(
                "Class Teacher Name",
                placeholder="Enter teacher's name",
                help="Name of the class teacher"
            )
            
            # Section (optional)
            section = st.text_input(
                "Section (Optional)",
                placeholder="e.g., A, B, C",
                help="Class section if applicable"
            )
        
        st.markdown("---")
        
        # Subject inputs
        st.subheader("📖 Subject-wise Diary Entries")
        st.markdown("*Enter homework, notes, or announcements for each subject*")
        
        # Define subjects
        subjects = {
            "📝 English": "english",
            "📜 Urdu": "urdu",
            "📐 Math": "math",
            "🔬 Science": "science",
            "🕌 Islamiat": "islamiat",
            "💻 Computer": "computer",
            "📖 Nazra": "nazra"
        }
        
        # Custom subject input
        st.markdown("### 🆕 Add Custom Subjects")
        st.markdown("*Add any additional subjects that are not in the list above*")
        
        col1_custom, col2_custom = st.columns(2)
        with col1_custom:
            new_subject1 = st.text_input("Custom Subject 1", key="custom_subject1")
            if new_subject1:
                subjects[f"🆕 {new_subject1}"] = new_subject1.lower()
        
        with col2_custom:
            new_subject2 = st.text_input("Custom Subject 2", key="custom_subject2")
            if new_subject2:
                subjects[f"🆕 {new_subject2}"] = new_subject2.lower()
        
        diary_entries = {}
        
        # Create two columns for subjects
        col1, col2 = st.columns(2)
        
        subject_items = list(subjects.items())
        mid_point = len(subject_items) // 2
        
        with col1:
            for subject_display, subject_key in subject_items[:mid_point]:
                diary_entries[subject_key] = st.text_area(
                    subject_display,
                    placeholder=f"Enter {subject_display.split()[-1]} homework/notes...",
                    height=100,
                    key=f"subject_{subject_key}"
                )
        
        with col2:
            for subject_display, subject_key in subject_items[mid_point:]:
                diary_entries[subject_key] = st.text_area(
                    subject_display,
                    placeholder=f"Enter {subject_display.split()[-1]} homework/notes...",
                    height=100,
                    key=f"subject_{subject_key}"
                )
        
        st.markdown("---")
        
        # Additional notes
        st.subheader("📌 Additional Notes")
        additional_notes = st.text_area(
            "General Notes/Announcements",
            placeholder="Any additional notes, announcements, or reminders...",
            height=80
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate PDF button
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🎯 Generate Diary PDF", use_container_width=True):
            # Validate inputs
            if not any(diary_entries.values()) and not additional_notes:
                st.markdown("""
                <div class="error-message">
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
                with st.spinner("🔄 Generating PDF..."):
                    pdf_path = generate_diary_pdf(diary_data)
                
                # Success message
                st.markdown("""
                <div class="success-message">
                    <strong>✅ Success!</strong> Diary PDF generated successfully!
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                with open(pdf_path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    
                    filename = f"diary_{selected_class.replace(' ', '_')}_{diary_date.strftime('%Y_%m_%d')}.pdf"
                    
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    <strong>❌ Error:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        <p>🏫 <strong>Al-Ghazali High School</strong> | Diary Management System</p>
        <p>Developed by IT Department • Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()