from flask import Flask, after_this_request
from flask_cors import CORS
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app = Flask(__name__)
app.config.from_object(config[config_name])

# Initialize extensions in order
# SQLAlchemy must be initialized before JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": app.config.get('ORIGINS', '127.0.0.1:3000')}})

# API Versioning - Add version header to all responses
@app.after_request
def add_api_version(response):
    """Add API version to all responses."""
    response.headers['API-Version'] = '1.0'
    response.headers['Content-Type'] = 'application/json'
    return response

# Import routes - must be after app and db initialization
from app import api_gateway

