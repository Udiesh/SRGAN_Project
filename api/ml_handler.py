import os
import numpy as np
from PIL import Image
import tensorflow as tf
from ISR.models import RRDN
from pathlib import Path

class MLHandler:
    def __init__(self):
        self.model = None
        self.initialized = False
        self.model_weights = 'gans'  # Using the pre-trained GANS weights
        
    def initialize(self):
        """Initialize the SRGAN model"""
        if not self.initialized:
            try:
                self.model = RRDN(weights=self.model_weights)
                self.initialized = True
                return True
            except Exception as e:
                print(f"Error initializing model: {str(e)}")
                return False
        return True

    def process_image(self, img):
        """Process an image through the SRGAN model"""
        if not self.initialized:
            if not self.initialize():
                raise Exception("Could not initialize model")

        # Convert PIL Image to numpy array
        img_array = np.array(img)
        
        # Ensure the image is in RGB format
        if len(img_array.shape) != 3 or img_array.shape[2] != 3:
            raise ValueError("Image must be RGB format")
            
        # Make prediction
        sr_img = self.model.predict(img_array)
        
        # Convert back to PIL Image
        sr_img = Image.fromarray(np.uint8(sr_img))
        return sr_img

# Create a global instance
ml_handler = MLHandler()