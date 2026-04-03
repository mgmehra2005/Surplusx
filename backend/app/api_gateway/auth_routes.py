from app import app
from flask import request, jsonify
from app.auth_service import loginWithEmail, loginWithUsername
from app.auth_service.registration import registerUser
from app.db_models.utils import _getUserRoleByUsername, _getUserRoleByEmail

print("Setting up authentication routes...")
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
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if "@" in username:
        login_status = loginWithEmail(username, password)
        if login_status:
            return jsonify({"message": "Login successful with email!", "role": _getUserRoleByEmail(username)}), 200
        else:
            return jsonify({"message": "Invalid email or password!"}), 401
    else:
        login_status = loginWithUsername(username, password)
        if login_status:
            return jsonify({"message": "Login successful with username!", "role": _getUserRoleByUsername(username)}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
        