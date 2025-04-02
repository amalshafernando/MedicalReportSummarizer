import requests
import json
API_TOKEN = "#####################################"  # Replace with your API key
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


def summarize_text(structured_text, max_length=150, min_length=50):
    """
    Summarize structured medical report text using Hugging Face's Inference API.
    Args:
        structured_text (dict): Dictionary with sections (e.g., "Diagnosis", "Treatment").
        max_length (int): Maximum length of the summary in tokens.
        min_length (int): Minimum length of the summary in tokens.
    Returns:
        dict: Summarized sections.
    """
    # Prepare the input text by combining sections with clear delimiters
    full_text = ""
    for section, content in structured_text.items():
        if content: 
            full_text += f"{section}:\n{content}\n\n"

    if not full_text.strip():
        return {"Summary": "No content available to summarize."}

   
    prompt = (
        "Summarize this medical report, focusing on key insights such as diagnosis, treatment, "
        "and recommendations. Retain medical terminology and ensure accuracy:\n\n" + full_text
    )

    # API payload
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False  # Deterministic output
        }
    }

    # Make the API request
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()

        # Extract the summary from the response
        if isinstance(result, list) and len(result) > 0:
            summary_text = result[0].get("summary_text", "Error: No summary generated.")
        else:
            summary_text = "Error: Unexpected API response."

    except requests.exceptions.RequestException as e:
        summary_text = f"Error: Failed to connect to summarization API - {str(e)}"

    # Structure the summary 
    summarized_data = {"Summary": summary_text}
    return summarized_data

if __name__ == "__main__":
    # Test  with sample
    sample_text = {
        "Patient Info": "Name: John Doe, Age: 45, ID: 12345",
        "Diagnosis": "Patient diagnosed with Type 2 Diabetes Mellitus.",
        "Treatment": "Prescribed Metformin 500mg daily.",
        "Recommendations": "Follow up in 3 months, monitor blood sugar levels."
    }
    summary = summarize_text(sample_text)
    print(json.dumps(summary, indent=2))