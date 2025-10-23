from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'SRGAN Project - Initial Test'

# Vercel requires this
app.debug = True