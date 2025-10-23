"""Test web routes."""
import io
import os
from PIL import Image

def test_index(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'OptimizedSRGAN' in response.data

def test_upscale_no_file(client):
    """Test upscale without file."""
    response = client.post('/upscale')
    assert response.status_code == 200
    assert b'No file part' in response.data

def test_upscale_empty_file(client):
    """Test upscale with empty file."""
    response = client.post('/upscale', data={'file': (io.BytesIO(), '')})
    assert response.status_code == 200
    assert b'No file selected' in response.data

def test_upscale_invalid_file(client):
    """Test upscale with invalid file type."""
    data = {'file': (io.BytesIO(b'test'), 'test.txt')}
    response = client.post('/upscale', data=data)
    assert response.status_code == 200
    assert b'File type not allowed' in response.data

def test_upscale_valid_file(client):
    """Test upscale with valid file."""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    
    data = {'file': (img_io, 'test.jpg')}
    response = client.post('/upscale', data=data)
    
    assert response.status_code == 200
    assert b'Enhancement Complete' in response.data