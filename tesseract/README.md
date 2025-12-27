# Image-OCR Backend

A Node.js backend service for extracting text from images using OCR (Optical Character Recognition) with Tesseract.js. This is completely free and runs locally without any API keys or cloud services.

## Features

- Accurate text extraction from images using Tesseract OCR engine
- Supports common image formats (JPEG, PNG, etc.)
- RESTful API with Express.js
- File upload handling with Multer
- Health check endpoint

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bethimanideep/Image-OCR.git
   cd Image-OCR
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

1. Start the server:
   ```bash
   npm start
   ```
   Or for development with auto-restart:
   ```bash
   npm run dev
   ```

2. The server will run on `http://localhost:3000`.

### API Endpoints

- **POST /ocr**: Extract text from an uploaded image.
  - **Request**: Multipart form-data with `image` field containing the image file.
  - **Response**: JSON with `text` field containing the extracted text.
  - **Example** (using curl):
    ```bash
    curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:3000/ocr
    ```

- **GET /health**: Health check endpoint.
  - **Response**: JSON with server status.

## Improving Accuracy

For better OCR accuracy:
- Use high-resolution images (at least 300 DPI)
- Ensure good contrast and lighting
- Pre-process images (e.g., convert to grayscale, remove noise)
- Use images with clear, standard fonts

## Dependencies

- [Express](https://expressjs.com/): Web framework
- [Multer](https://github.com/expressjs/multer): File upload middleware
- [Tesseract.js](https://github.com/naptha/tesseract.js/): OCR engine

## License

MIT
