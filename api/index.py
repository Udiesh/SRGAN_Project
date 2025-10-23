from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'SRGAN API is running',
        'endpoints': {
            'upscale': '/api/upscale',
            'status': '/api/status'
        }
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'success',
        'service': 'online',
        'version': '1.0.0'
    })

@app.route('/api/upscale', methods=['POST'])
def upscale():
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file provided'
        }), 400
        
    return jsonify({
        'status': 'success',
        'message': 'File upload endpoint ready',
        'stage': 'development'
    })

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