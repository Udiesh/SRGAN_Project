"""Image processing service."""
import os
import numpy as np
from PIL import Image
from ISR.models import RRDN
from flask import current_app
import uuid
import time

class ImageProcessor:
    """Image processing service class."""
    
    def __init__(self):
        """Initialize the image processor."""
        self.model = None
    
    def init_model(self, weights='gans'):
        """Initialize the RRDN model."""
        if self.model is None:
            self.model = RRDN(weights=weights)
    
    def process_image(self, image_file, patch_size=100):
        """Process an image file and return the enhanced version."""
        try:
            # Generate unique filename
            timestamp = int(time.time())
            unique_id = str(uuid.uuid4())[:8]
            original_name = os.path.splitext(image_file.filename)[0]
            ext = os.path.splitext(image_file.filename)[1]
            
            input_filename = f"{original_name}_{timestamp}_{unique_id}{ext}"
            output_filename = f"sr_{original_name}_{timestamp}_{unique_id}{ext}"
            
            input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], input_filename)
            output_path = os.path.join(current_app.config['RESULT_FOLDER'], output_filename)
            
            # Save input image
            image_file.save(input_path)
            
            # Process image
            img = Image.open(input_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            lr_img = np.array(img)
            sr_img = self.model.predict(lr_img, by_patch_of_size=patch_size)
            
            # Save result
            Image.fromarray(sr_img).save(output_path)
            
            # Get image info
            original_size = img.size
            enhanced_size = (sr_img.shape[1], sr_img.shape[0])
            width_ratio = sr_img.shape[1] / original_size[0]
            height_ratio = sr_img.shape[0] / original_size[1]
            upscale_ratio = round((width_ratio + height_ratio) / 2, 1)
            
            return {
                'success': True,
                'input_filename': input_filename,
                'output_filename': output_filename,
                'original_size': f"{original_size[0]} × {original_size[1]}",
                'enhanced_size': f"{enhanced_size[0]} × {enhanced_size[1]}",
                'upscale_ratio': f"{upscale_ratio}x"
            }
            
        except Exception as e:
            current_app.logger.error(f"Error processing image: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Global image processor instance
image_processor = ImageProcessor()

def init_model(app):
    """Initialize the model with application context."""
    with app.app_context():
        image_processor.init_model(app.config['MODEL_WEIGHTS'])