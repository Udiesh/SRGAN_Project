# OptimizedSRGAN Image Super Resolution

A web application that uses SRGAN (Super Resolution Generative Adversarial Network) to enhance image resolution by 4x.

## Key Features

- 4x image upscaling using advanced GAN architecture
- Built on RRDN model with GAN-optimized weights
- Simple and intuitive user interface
- Flask-based web application

## Project Structure

```
.
├── app.py                  # Flask web application
├── requirements.txt        # Python dependencies
├── fixed_generator.h5      # Model weights
├── static/                 # Static files for web app
│   ├── results/            # Enhanced images
│   └── uploads/            # Original uploaded images
├── templates/              # HTML templates
│   ├── index.html          # Upload page
│   └── result.html         # Results page
└── ISR/                    # Image Super Resolution package
```

## Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## How It Works

The application uses a pre-trained SRGAN model to upscale images. Upload an image through the web interface, and the model will process it to create a 4x larger version with enhanced details.

## Technical Implementation

The implementation uses TensorFlow and the ISR (Image Super Resolution) library with an optimized RRDN model architecture trained with GAN techniques for better perceptual quality.
