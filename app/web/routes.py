"""Web routes module."""
from flask import Blueprint, render_template, request, current_app, url_for
from werkzeug.utils import secure_filename
from ..services.image_processor import image_processor
from flask_limiter.util import get_remote_address
from ..extensions import limiter

web_bp = Blueprint('web', __name__)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@web_bp.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@web_bp.route('/upscale', methods=['POST'])
@limiter.limit("5 per minute")
def upscale():
    """Handle image upload and processing."""
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')
    
    if not allowed_file(file.filename):
        return render_template('index.html', 
                             error='File type not allowed. Please use PNG, JPG, or JPEG.')
    
    try:
        result = image_processor.process_image(file)
        
        if not result['success']:
            raise Exception(result['error'])
        
        return render_template('result.html',
                             original=url_for('static', 
                                            filename=f'uploads/{result["input_filename"]}'),
                             result=url_for('static', 
                                          filename=f'results/{result["output_filename"]}'),
                             original_size=result['original_size'],
                             enhanced_size=result['enhanced_size'],
                             upscale_ratio=result['upscale_ratio'])
    
    except Exception as e:
        current_app.logger.error(f"Error in upscale route: {str(e)}")
        return render_template('index.html', error=f'Error processing image: {str(e)}')