const express = require('express');
const multer = require('multer');
const { createWorker } = require('tesseract.js');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 4000;

// Enable CORS for all routes
app.use(cors());

// Configure multer for file uploads
const upload = multer({
  dest: 'uploads/', // Directory to save uploaded files
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB limit
  fileFilter: (req, file, cb) => {
    // Accept only image files
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed!'), false);
    }
  }
});

// Create uploads directory if it doesn't exist
const fs = require('fs');
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

// OCR endpoint
app.post('/ocr', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No image file provided' });
    }

    const imagePath = req.file.path;

    // Create Tesseract worker
    const worker = await createWorker();

    // Load English language (you can add more languages if needed)
    await worker.loadLanguage('eng');
    await worker.initialize('eng');

    // Recognize text from image
    const { data: { text } } = await worker.recognize(imagePath);

    // Terminate worker
    await worker.terminate();

    // Clean up uploaded file
    fs.unlinkSync(imagePath);

    // Return extracted text
    res.json({ text: text.trim() });

  } catch (error) {
    console.error('OCR Error:', error);
    res.status(500).json({ error: 'Failed to extract text from image' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', message: 'OCR Backend is running' });
});

// Start server
app.listen(port, () => {
  console.log(`OCR Backend server running on port ${port}`);
});