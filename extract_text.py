import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file. Uses PyMuPDF for native PDFs and Tesseract OCR for scanned PDFs.
    Returns the extracted text as a string.
    """
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        if text.strip():
            extracted_text += text + "\n"
        else:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            extracted_text += ocr_text + "\n"

    pdf_document.close()
    return extracted_text if extracted_text else "No text could be extracted."

def preprocess_text(raw_text):
    """
    Clean and structure the extracted text into sections.
    Returns a dictionary with structured data.
    """
    # Clean the text: remove page markers and extra whitespace
    cleaned_text = re.sub(r'Page \d+( \(OCR\))?:', '', raw_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
    lines = cleaned_text.split('\n')

    # Define section keywords (case-insensitive)
 
    structured_data = {
        "Patient Info": "",
        "Diagnosis": "",
        "Treatment": "",
        "Recommendations": "",
        "Other": ""
    }
    section_keywords = {
        "Patient Info": ["patient", "name", "age", "id"],
        "Diagnosis": ["diagnosis", "condition", "findings"],
        "Treatment": ["treatment", "therapy", "medication"],
        "Recommendations": ["recommendation", "follow", "plan"]
    }

    current_section = "Other"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for section keywords
        line_lower = line.lower()
        section_assigned = False
        for section, keywords in section_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                current_section = section
                section_assigned = True
                break
        
        # Add the line to the current section
        structured_data[current_section] += line + "\n"

    # Remove empty sections and trailing newlines
    return {k: v.strip() for k, v in structured_data.items() if v.strip()}