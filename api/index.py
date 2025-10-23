from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image
import os
import io
import uuid
import time
from ml_handler import ml_handler

app = Flask(__name__)
CORS(app)

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Initialize ML model
ml_handler.initialize()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'SRGAN API is running',
        'endpoints': {
            'upscale': '/api/upscale',
            'status': '/api/status'
        },
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'max_size': '16MB'
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'success',
        'service': 'online',
        'version': '1.0.0',
        'features': {
            'image_upload': True,
            'image_processing': True,
            'super_resolution': True,
            'model_initialized': ml_handler.initialized
        }
    })

@app.route('/api/upscale', methods=['POST'])
def upscale():
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No file selected'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': f'File type not allowed. Supported types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Read and validate the image
        img = Image.open(file.stream)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get original dimensions
        orig_width, orig_height = img.size
        
        # Process image through SRGAN
        start_time = time.time()
        sr_img = ml_handler.process_image(img)
        process_time = time.time() - start_time
        
        # Get enhanced dimensions
        new_width, new_height = sr_img.size
        
        # Convert to bytes for response
        img_byte_arr = io.BytesIO()
        sr_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Send the processed image
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='enhanced.png',
            headers={
                'X-Original-Width': str(orig_width),
                'X-Original-Height': str(orig_height),
                'X-Enhanced-Width': str(new_width),
                'X-Enhanced-Height': str(new_height),
                'X-Process-Time': str(round(process_time, 2)),
                'X-Enhancement-Factor': str(new_width / orig_width)
            }
        )
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing image: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

# Vercel requires this
app.debug = True