"""WSGI entry point."""
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    app = create_app('production')
except Exception as e:
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'status': 'error',
            'message': 'Application failed to start',
            'error': str(e)
        }), 500