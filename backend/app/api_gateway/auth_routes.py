from app import app
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.auth_service import loginWithEmail, registerUser
from app.utils import normalize_email, sanitize_input
import logging

logger = logging.getLogger(__name__)

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user account.
    
    BUG FIX #1: Added register endpoint for new user registration
    
    Request JSON:
    {
        "email": "user@example.com",
        "name": "John Doe",
        "password": "password123",
        "role": "DONOR"  # optional, defaults to DONOR
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Request body is required"}), 400
    
    email = normalize_email(data.get('email', ''))
    name = sanitize_input(data.get('name', ''), max_length=100)
    password = data.get('password', '')
    role = data.get('role', 'DONOR').upper()
    
    # Call registerUser from auth_service
    result = registerUser(email, name, password, role)
    
    if result['success']:
        return jsonify({
            "message": result['message'],
            "user": result['user']
        }), 201
    else:
        return jsonify({"message": result['message']}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with email and password to receive JWT token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "Invalid request format"}), 400
        
        email = normalize_email(data.get('email', ''))
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"message": "Email and password required"}), 400
        
        user_data = loginWithEmail(email, password)
        if user_data:
            access_token = create_access_token(identity=user_data['uid'])
            return jsonify({
                "message": "Login successful",
                "token": access_token,
                "user": {
                    "uid": user_data['uid'],
                    "name": user_data['name'],
                    "email": user_data['email'],
                    "role": user_data['role']
                }
            }), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({"message": "Login failed. Please try again."}), 500