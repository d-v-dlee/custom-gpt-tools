from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract
import io
import os

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr_api():
    """
    OCR API endpoint that accepts an image or PDF file as input and returns the extracted text.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext == '.pdf':
        images = convert_from_bytes(file.read())
        extracted_texts = [pytesseract.image_to_string(image) for image in images]
    else:
        image = Image.open(file.stream)
        extracted_texts = [pytesseract.image_to_string(image)]
    
    # return dict where key is page number and value is extracted text
    extracted_dict = {i+1: text for i, text in enumerate(extracted_texts)}

    return extracted_dict

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.', 'ai-plugin.json', mimetype='application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
    app.run()