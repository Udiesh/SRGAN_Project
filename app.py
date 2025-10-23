import os
import numpy as np
import time
from flask import Flask, request, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from ISR.models import RRDN

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file uploads to 16MB

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Use RRDN with gans weights for best quality
model = None

def get_model():
    global model
    if model is None:
        # Initialize the model once and reuse it
        model = RRDN(weights='gans')
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')
    
    if not allowed_file(file.filename):
        return render_template('index.html', error='File type not allowed. Please use PNG, JPG, or JPEG.')
    
    # Save the uploaded file with timestamp to prevent caching issues
    base_filename = secure_filename(file.filename)
    name, ext = os.path.splitext(base_filename)
    timestamp = int(time.time())
    filename = f"{name}_{timestamp}{ext}"
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Convert to RGB if the image has an alpha channel or is not in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array for model processing
        lr_img = np.array(img)
        
        # Get the model and predict
        sr_model = get_model()
        
        # Process with model
        patch_size = 100
        sr_img = sr_model.predict(lr_img, by_patch_of_size=patch_size)
        
        # Save the result
        output_filename = f"sr_{name}_{timestamp}{ext}"
        output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
        Image.fromarray(sr_img).save(output_path)
        
        # Get image dimensions for display
        original_size = img.size
        enhanced_size = f"{sr_img.shape[1]} × {sr_img.shape[0]}"
        
        # Calculate upscale ratio
        width_ratio = sr_img.shape[1] / original_size[0]
        height_ratio = sr_img.shape[0] / original_size[1]
        upscale_ratio = round((width_ratio + height_ratio) / 2, 1)
        
        return render_template('result.html', 
                              original=url_for('static', filename=f'uploads/{filename}'),
                              result=url_for('static', filename=f'results/{output_filename}'),
                              original_size=f"{original_size[0]} × {original_size[1]}",
                              enhanced_size=f"{sr_img.shape[1]} × {sr_img.shape[0]}",
                              upscale_ratio=f"{upscale_ratio}x")
    
    except Exception as e:
        # Log the original error for debugging
        print(f"Error processing image: {str(e)}")
        
        return render_template('index.html', error=f'Error processing image: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True) 