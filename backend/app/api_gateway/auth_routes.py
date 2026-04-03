from app import app
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.auth_service import loginWithEmail, loginWithUsername
from app.auth_service.registration import registerUser
from app.db_models.utils import _getUserRoleByUsername, _getUserRoleByEmail
from app.utils import normalize_email, sanitize_input

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
    """Login with username or email.
    
    BUG FIX: Now returns JWT token in response
    
    Request JSON:
    {
        "username": "user@example.com" or "username",
        "password": "password123"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Request body is required"}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"message": "Username/email and password are required"}), 400
    
    if "@" in username:
        # Login with email
        login_status = loginWithEmail(username, password)
        if login_status:
            role = _getUserRoleByEmail(username)
            token = create_access_token(identity=username)
            return jsonify({
                "message": "Login successful with email!",
                "token": token,
                "username": username,
                "email": username,
                "role": role
            }), 200
        else:
            return jsonify({"message": "Invalid email or password!"}), 401
    else:
        # Login with username
        login_status = loginWithUsername(username, password)
        if login_status:
            role = _getUserRoleByUsername(username)
            token = create_access_token(identity=username)
            return jsonify({
                "message": "Login successful with username!",
                "token": token,
                "username": username,
                "role": role
            }), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
        