from flask import Flask, after_this_request
from flask_cors import CORS
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

# Import Flask-Migrate if available (for database migrations)
try:
    from flask_migrate import Migrate
    migrate_available = True
except ImportError:
    migrate_available = False

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app = Flask(__name__)
app.config.from_object(config[config_name])
CORS(app, resources={r"/api/*": {"origins": app.config.get('ORIGINS', '127.0.0.1:3000')}})

db = SQLAlchemy(app)

# Initialize Flask-Migrate if available
if migrate_available:
    migrate = Migrate(app, db)

from app import api_gateway

