from app import app
from flask import request, jsonify
from app.auth_service import loginWithEmail, loginWithUsername
from app.auth_service.registration import registerUser

print("Setting up authentication routes...")
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    fname = data.get('firstName')
    lname = data.get('lastName')
    full_name = f"{fname} {lname}".strip()
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')
    password = data.get('password')

    _registereduserResponse = registerUser(username, email, password, role, phone, full_name)
    if _registereduserResponse:
        return jsonify({"message": "User registered successfully", "data": data}), 201
    else:
        return jsonify({"message": "User Not registered", "data": data})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if "@" in username:
        login_status = loginWithEmail(username, password)
        if login_status:
            return jsonify({"message": "Login successful with email!"}), 200
        else:
            return jsonify({"message": "Invalid email or password!"}), 401
    else:
        login_status = loginWithUsername(username, password)
        if login_status:
            return jsonify({"message": "Login successful with username!"}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
        