"""Test configuration."""
import os
import tempfile
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create application for the tests."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    
    # other setup can go here
    
    yield app
    
    # clean up / reset resources here
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()