"""WSGI entry point."""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'SRGAN Project - Initial Deployment Test'

if __name__ == '__main__':
    app.run()