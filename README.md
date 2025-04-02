# Medical Report Summarizer

A Flask-based web application to upload medical PDF reports, extract text (including from scanned documents), summarize content using a fine-tuned Mistral-7B model, and display results in a user-friendly interface. The project ensures HIPAA/GDPR compliance through anonymization and provides a REST API for programmatic access.

## Features
- **PDF Text Extraction**: Extracts text from native and scanned PDFs using PyMuPDF and Tesseract OCR.
- **Text Preprocessing**: Structures text into sections (e.g., Patient Info, Diagnosis) and anonymizes PII.
- **Summarization**: Uses a fine-tuned Mistral-7B model to generate concise summaries, with a fallback to the base model.
- **Web Interface**: Upload PDFs via `index.html` and view summaries on `summary.html`.
- **REST API**: Summarize PDFs programmatically via `/api/summarize`.
- **Training**: Collect training data through the UI and fine-tune the model with LoRA.

## Project Structure
MedicalReportSummarizer/
│
├── app.py                 # Flask app with routes
├── extract_text.py        # Text extraction and preprocessing
├── summarize_text.py      # Summarization with Mistral-7B
├── train_model.py         # Fine-tuning script
├── templates/
│   ├── index.html         # Upload page
│   └── summary.html       # Summary display page
├── uploads/               # Temporary folder for PDFs
├── training_data.json     # Stores training data
└── requirements.txt       # Dependencies


## Prerequisites
- **Python 3.8+**
- **Tesseract OCR**: Installed and added to PATH (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe` on Windows).
- **GPU (Optional)**: For faster model training and inference (e.g., NVIDIA GPU with CUDA).

## Setup
1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd MedicalReportSummarizer
