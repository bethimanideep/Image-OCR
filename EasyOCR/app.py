from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import easyocr
import os
from PIL import Image
import io

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

# Initialize EasyOCR reader (English by default, can add more languages)
reader = easyocr.Reader(['en'])

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Perform OCR
            results = reader.readtext(filepath, detail=0)  # detail=0 returns only text
            text = ' '.join(results).strip()

            # Clean up
            os.remove(filepath)

            return jsonify({'text': text or 'No text found in the image'})

        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'Python OCR Backend is running'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)