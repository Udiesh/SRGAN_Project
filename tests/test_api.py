"""Test API routes."""
import io
from PIL import Image

def test_api_upscale_no_file(client):
    """Test API upscale without file."""
    response = client.post('/api/upscale')
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert 'No file part' in json_data['error']

def test_api_upscale_empty_file(client):
    """Test API upscale with empty file."""
    response = client.post('/api/upscale', data={'file': (io.BytesIO(), '')})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert 'No file selected' in json_data['error']

def test_api_upscale_invalid_file(client):
    """Test API upscale with invalid file type."""
    data = {'file': (io.BytesIO(b'test'), 'test.txt')}
    response = client.post('/api/upscale', data=data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert 'File type not allowed' in json_data['error']

def test_api_upscale_valid_file(client):
    """Test API upscale with valid file."""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)
    
    data = {'file': (img_io, 'test.jpg')}
    response = client.post('/api/upscale', data=data)
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'data' in json_data
    assert 'input_url' in json_data['data']
    assert 'output_url' in json_data['data']