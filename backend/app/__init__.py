from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

from app import api_gateway

