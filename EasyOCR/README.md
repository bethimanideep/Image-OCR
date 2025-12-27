# Python OCR Backend

A Python Flask backend for extracting text from images using OCR with EasyOCR. EasyOCR is a deep learning-based OCR tool that provides high accuracy for various languages and image types.

## Features

- Accurate text extraction using EasyOCR (deep learning models)
- RESTful API with Flask
- Supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
- File upload handling
- Health check endpoint

## Installation

1. Navigate to the python folder:
   ```bash
   cd python
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Note: EasyOCR will download models on first use (may take time).

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. The server will run on `http://localhost:5000`.

### API Endpoints

- **POST /ocr**: Extract text from an uploaded image.
  - **Request**: Multipart form-data with `image` field containing the image file.
  - **Response**: JSON with `text` field containing the extracted text.
  - **Example** (using curl):
    ```bash
    curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/ocr
    ```

- **GET /health**: Health check endpoint.
  - **Response**: JSON with server status.

## Improving Accuracy

For better OCR accuracy:
- Use high-resolution images (at least 300 DPI)
- Ensure good contrast and lighting
- Avoid skewed or distorted text
- EasyOCR handles multiple languages—add language codes to the reader initialization if needed (e.g., `['en', 'fr']`)

## Dependencies

- [EasyOCR](https://github.com/JaidedAI/EasyOCR): Deep learning-based OCR engine
- [Flask](https://flask.palletsprojects.com/): Web framework
- [Werkzeug](https://werkzeug.palletsprojects.com/): WSGI utility library
- [Pillow](https://python-pillow.org/): Image processing library

## License

MIT