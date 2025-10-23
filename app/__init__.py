"""Application factory module."""
import os
from flask import Flask
from .config import config
from .extensions import csrf, limiter, init_logging
from .services.image_processor import init_model
from .web.routes import web_bp
from .api.routes import api_bp

def create_app(config_name=None):
    """Create Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure the upload and result folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    # Initialize extensions
    csrf.init_app(app)
    limiter.init_app(app)
    init_logging(app)
    init_model(app)

    # Register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app