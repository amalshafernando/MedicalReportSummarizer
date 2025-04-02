from flask import Flask, request, render_template, jsonify
import os
from extract_text import extract_text_from_pdf, preprocess_text
from summarize_text import summarize_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded!"
        file = request.files['file']
        if file.filename == '':
            return "No file selected!"
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Extract and preprocess text
            raw_text = extract_text_from_pdf(filepath)
            structured_text = preprocess_text(raw_text)
            
            return render_template('result.html', structured_text=structured_text, summarized_text=None)
    
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    structured_text = data.get('structured_text', {})
    summarized_text = summarize_text(structured_text)
    return jsonify({'summary': summarized_text['Summary']})

if __name__ == '__main__':
    app.run(debug=True)