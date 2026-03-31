from flask import Flask
from flask_cors import CORS
from config import config
from flask_sqlalchemy import SQLAlchemy

config_name = 'default'
app = Flask(__name__)
app.config.from_object(config[config_name])
CORS(app, resources={r"/api/*": {"origins": app.config.get('ORIGINS', '127.0.0.1:3000')}})

db = SQLAlchemy(app)

from app import api_gateway

