from app import app
from flask import request, jsonify
from app.auth_service import loginWithEmail, loginWithUsername
from app.auth_service.registration import registerUser
from app.db_models.utils import _getUserRoleByUsername, _getUserRoleByEmail

print("Setting up authentication routes...")
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    fname = data.get('firstName')
    lname = data.get('lastName')
    full_name = f"{fname} {lname}".strip()
    email = data.get('email').lower()
    phone = data.get('phone')
    role = data.get('role')
    password = data.get('password')

    _registereduserResponse = registerUser(username, email, password, role, phone, full_name)
    if _registereduserResponse:
        return jsonify({"message": "User registered successfully", "role": role}), 201
    else:
        return jsonify({"message": "User Not registered"})

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
        