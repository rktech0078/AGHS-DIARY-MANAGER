# 📚 School Diary Manager

A modern, professional web application for generating daily class diary PDFs using Python and Streamlit.

## 🌟 Features

- **Modern UI**: Clean, professional Streamlit interface with custom styling
- **Multi-Class Support**: Generate diaries for grades 1st through 10th
- **Subject Management**: Dedicated fields for all major subjects
- **Professional PDFs**: Business letterhead-style PDF generation
- **Easy Download**: One-click PDF download functionality
- **Responsive Design**: Works well on desktop and tablet devices

## 🏗️ Project Structure

```
diary_manager/
├── main.py                 # Main Streamlit application
├── utils/
│   └── pdf_generator.py   # PDF generation logic
├── assets/
│   └── school_logo.png    # School logo (optional)
├── output/                # Generated PDF files
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
Download the project files to your local machine.

### Step 2: Install Dependencies
```bash
cd diary_manager
pip install -r requirements.txt
```

### Step 3: Add School Logo (Optional)
Place your school logo as `school_logo.png` in the `assets/` folder. The logo should be in PNG format and ideally square (recommended: 200x200 pixels).

### Step 4: Run the Application
```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 How to Use

1. **Open the Application**: Launch the app using the command above
2. **Enter Basic Information**:
   - Select the date (defaults to today)
   - Choose the class from dropdown
   - Enter teacher name and section (optional)
3. **Fill Subject Entries**:
   - Add homework, notes, or announcements for each subject
   - Subjects include: English, Urdu, Math, Science, Islamiat, Computer, Nazra
4. **Add Additional Notes**: Include any general announcements or reminders
5. **Generate PDF**: Click "Generate Diary PDF" button
6. **Download**: Use the download button to save the PDF file

## 🎨 PDF Features

The generated PDFs include:
- **Professional Header**: School name and "Daily Class Diary" title
- **Class Information**: Date, class, teacher details in a formatted table
- **Subject Sections**: Each subject clearly labeled with emoji icons
- **Clean Formatting**: Proper spacing, fonts, and colors
- **School Branding**: Logo integration and school footer
- **Page Decorations**: Borders, watermarks, and page numbers

## 🛠️ Customization

### Changing School Information
Edit the following in `main.py`:
- School name in the header section
- Footer text with school name

### Adding New Subjects
In `main.py`, modify the `subjects` dictionary:
```python
subjects = {
    "📝 English": "english",
    "📜 Urdu": "urdu",
    "🆕 New Subject": "new_subject",
    # Add more subjects here
}
```

### Modifying PDF Layout
Edit `utils/pdf_generator.py` to:
- Change colors (modify HexColor values)
- Adjust fonts and sizes
- Modify spacing and layout
- Add new sections

### Custom Styling
Modify the CSS in `main.py` to change:
- Color schemes
- Button styles
- Form layouts
- Typography

## 📋 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 100MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge

## 🔧 Troubleshooting

### Common Issues

1. **ImportError**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Logo not showing**: Ensure `school_logo.png` exists in `assets/` folder

3. **PDF generation fails**: Check that the `output/` directory exists and is writable

4. **Port already in use**: If port 8501 is busy, specify a different port:
   ```bash
   streamlit run main.py --server.port 8502
   ```

### Error Messages
- **"Please enter at least one subject entry"**: Fill in at least one subject field
- **PDF generation error**: Check file permissions in the output directory

## 📝 Version History

- **v1.0.0**: Initial release with basic diary generation
- Professional PDF layout with school branding
- Multi-subject support with clean UI

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical support or feature requests:
- Check the troubleshooting section above
- Review the code comments for implementation details
- Test with sample data to identify issues

## 📄 License

This project is developed for educational purposes. Feel free to modify and adapt for your school's needs.

---

**Developed by IT Department - Al-Ghazali High School**  
*Making school administration easier, one diary at a time* 📖