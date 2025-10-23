"""Application configuration."""
import os
from datetime import timedelta

class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    RESULT_FOLDER = os.path.join('static', 'results')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Security
    WTF_CSRF_ENABLED = True
    RATELIMIT_DEFAULT = "5 per minute"
    
    # Logging
    LOG_FOLDER = "logs"
    LOG_LEVEL = "INFO"
    
    # Model
    MODEL_WEIGHTS = 'gans'
    PATCH_SIZE = 100
    
class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Override these in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')

class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}