# PaddleOCR Backend

A Python Flask backend for extracting text from images using OCR with PaddleOCR. PaddleOCR is Baidu's deep learning-based OCR toolkit, providing high accuracy for text detection and recognition.

## Features

- High-accuracy text extraction using PaddleOCR (deep learning models)
- RESTful API with Flask
- Supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
- File upload handling
- Health check endpoint

## Installation

1. Navigate to the PaddleOCR folder:
   ```bash
   cd PaddleOCR
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Note: PaddleOCR will download models on first use (may take time and require internet).

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. The server will run on `http://localhost:4000`.

### API Endpoints

- **POST /ocr**: Extract text from an uploaded image.
  - **Request**: Multipart form-data with `image` field containing the image file.
  - **Response**: JSON with `text` field containing the extracted text.
  - **Example** (using curl):
    ```bash
    curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:4000/ocr
    ```

- **GET /health**: Health check endpoint.
  - **Response**: JSON with server status.

## Improving Accuracy

For better OCR accuracy:
- Use high-resolution images (at least 300 DPI)
- Ensure good contrast and lighting
- PaddleOCR handles angles and orientations automatically
- For multi-language, change `lang` parameter (e.g., `lang='ch'` for Chinese)

## Dependencies

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR): Baidu's OCR toolkit
- [PaddlePaddle](https://www.paddlepaddle.org.cn/): Deep learning framework
- [Flask](https://flask.palletsprojects.com/): Web framework
- [Werkzeug](https://werkzeug.palletsprojects.com/): WSGI utility library
- [Pillow](https://python-pillow.org/): Image processing library

## License

MIT