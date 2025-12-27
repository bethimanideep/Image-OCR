import os
import sys
import tempfile
import traceback
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR

app = Flask(__name__)

# Enable verbose logging for debugging
print("Initializing PaddleOCR...", file=sys.stderr)

try:
    # Try different initialization options
    ocr = PaddleOCR(
        lang='en',
        use_angle_cls=False,  # Try False first
        show_log=True,  # Enable logs to see what's happening
        use_gpu=False,
        rec_image_shape='3, 48, 320'
    )
    print("✓ PaddleOCR initialized successfully", file=sys.stderr)
except Exception as e:
    print(f"✗ PaddleOCR initialization failed: {e}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    ocr = None

@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    print(f"\n=== OCR Request Received ===", file=sys.stderr)
    
    if ocr is None:
        print("OCR engine not initialized", file=sys.stderr)
        return jsonify({'error': 'OCR engine not initialized'}), 500
    
    if 'image' not in request.files:
        print("No 'image' field in request", file=sys.stderr)
        return jsonify({'error': 'No image file provided. Use form-data with key "image"'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        print("Empty filename", file=sys.stderr)
        return jsonify({'error': 'No file selected'}), 400
    
    print(f"Processing file: {file.filename}", file=sys.stderr)
    
    temp_file_path = None
    try:
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if not file_ext:
            file_ext = '.jpg'
        
        # Save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            file.save(tmp.name)
            temp_file_path = tmp.name
        
        print(f"File saved to: {temp_file_path}", file=sys.stderr)
        print(f"File size: {os.path.getsize(temp_file_path)} bytes", file=sys.stderr)
        
        # Test if it's a valid image by trying to read it
        try:
            from PIL import Image
            img = Image.open(temp_file_path)
            print(f"Image info: {img.format}, {img.size}, {img.mode}", file=sys.stderr)
            img.verify()  # Verify it's a valid image
            img = Image.open(temp_file_path)  # Reopen after verify
        except Exception as img_error:
            print(f"Invalid image file: {img_error}", file=sys.stderr)
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Try OCR
        print("Starting OCR processing...", file=sys.stderr)
        
        # Try different methods
        try:
            # Method 1: Using predict with file path
            result = ocr.ocr(temp_file_path, cls=False)
            print(f"OCR method 1 completed", file=sys.stderr)
        except Exception as method1_error:
            print(f"Method 1 failed: {method1_error}", file=sys.stderr)
            try:
                # Method 2: Using img array directly
                import numpy as np
                from PIL import Image
                img = Image.open(temp_file_path).convert('RGB')
                img_array = np.array(img)
                result = ocr.ocr(img_array, cls=False)
                print(f"OCR method 2 completed", file=sys.stderr)
            except Exception as method2_error:
                print(f"Method 2 failed: {method2_error}", file=sys.stderr)
                result = None
        
        print(f"OCR result type: {type(result)}", file=sys.stderr)
        
        if result:
            print(f"OCR result structure: {len(result) if hasattr(result, '__len__') else 'no length'}", file=sys.stderr)
            
            # Extract text
            text_list = []
            detailed_results = []
            
            if isinstance(result, list) and len(result) > 0:
                for page_num, page in enumerate(result):
                    if page:
                        for line_num, line in enumerate(page):
                            if line and len(line) >= 2:
                                # Get coordinates and text
                                coords = line[0]
                                text_info = line[1]
                                text = text_info[0] if len(text_info) > 0 else ""
                                confidence = float(text_info[1]) if len(text_info) > 1 else 0.0
                                
                                text_list.append(text)
                                detailed_results.append({
                                    'text': text,
                                    'confidence': confidence,
                                    'page': page_num + 1,
                                    'line': line_num + 1
                                })
                                print(f"Detected: '{text}' (conf: {confidence:.2f})", file=sys.stderr)
            
            full_text = ' '.join(text_list)
            print(f"Extracted {len(text_list)} words", file=sys.stderr)
            
            return jsonify({
                'success': True,
                'text': full_text,
                'words': text_list,
                'detailed': detailed_results,
                'word_count': len(text_list)
            })
        else:
            print("No OCR result returned", file=sys.stderr)
            return jsonify({
                'success': True,
                'text': '',
                'words': [],
                'message': 'No text detected in image'
            })
            
    except Exception as e:
        print(f"ERROR in OCR processing: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return jsonify({
            'success': False,
            'error': 'Processing failed',
            'message': str(e),
            'traceback': traceback.format_exc().split('\n')
        }), 500
    
    finally:
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                print(f"Cleaned up temp file: {temp_file_path}", file=sys.stderr)
            except:
                pass

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'running' if ocr else 'error',
        'ocr_initialized': ocr is not None,
        'python_version': sys.version
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({'message': 'API is working'})

if __name__ == '__main__':
    print("\nStarting Flask server on http://0.0.0.0:4000", file=sys.stderr)
    app.run(host='0.0.0.0', port=4000, debug=True)  # Enable debug for more info