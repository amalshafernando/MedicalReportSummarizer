from flask import Flask, request, render_template
import os
from extract_text import extract_text_from_pdf, preprocess_text

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
            
            return render_template('result.html', structured_text=structured_text)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
