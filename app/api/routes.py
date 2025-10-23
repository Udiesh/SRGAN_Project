"""API routes module."""
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from ..services.image_processor import image_processor
from ..extensions import limiter
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/upscale', methods=['POST'])
@limiter.limit("20 per hour")
def upscale():
    """API endpoint for image upscaling."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({
            'error': 'File type not allowed. Please use PNG, JPG, or JPEG.'
        }), 400
    
    try:
        result = image_processor.process_image(file)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 500
            
        return jsonify({
            'status': 'success',
            'data': {
                'input_url': f'/static/uploads/{result["input_filename"]}',
                'output_url': f'/static/results/{result["output_filename"]}',
                'original_size': result['original_size'],
                'enhanced_size': result['enhanced_size'],
                'upscale_ratio': result['upscale_ratio']
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"API Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']