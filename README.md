# Medical Report Summarizer

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-API-orange.svg)

A web-based tool to extract text from medical/healthcare PDF reports and generate concise summaries using a Large Language Model (LLM) via Hugging Face's Inference API. Built with Flask, PyMuPDF, Tesseract OCR, and Bootstrap for a user-friendly interface.

## Features
- **PDF Text Extraction:** Extracts text from both native and scanned PDFs using PyMuPDF and Tesseract OCR.
- **Text Preprocessing:** Structures extracted text into sections (e.g., Patient Info, Diagnosis, Treatment).
- **LLM Summarization:** Summarizes medical reports using Hugging Face's pre-trained models (e.g., BART).
- **Web Interface:** Upload PDFs and view extracted text and summaries via a Flask-based UI.
- **Compliance Ready:** Designed with HIPAA/GDPR in mind (anonymization can be added).


![Upload PDF](https://github.com/amalshafernando/MedicalReportSummarizer/blob/main/screenshots/ui%201.png)
![Extract and summarize data](https://github.com/amalshafernando/MedicalReportSummarizer/blob/main/screenshots/ui%202.png)
