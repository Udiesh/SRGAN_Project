from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image
import os
import io
import uuid
import time

app = Flask(__name__)
CORS(app)

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

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
            'image_processing': False,  # Will be True when ML is added
            'super_resolution': False   # Will be True when SRGAN is added
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
        width, height = img.size
        
        # For now, just return the original image with metadata
        # Later, this is where we'll add the SRGAN processing
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return jsonify({
            'status': 'success',
            'message': 'Image processed successfully',
            'metadata': {
                'original_width': width,
                'original_height': height,
                'format': img.format,
                'mode': img.mode
            },
            'note': 'ML processing will be added in the next update'
        })
        
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