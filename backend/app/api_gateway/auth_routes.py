from app import app
from flask import request, jsonify
from app.auth_service import loginWithEmail, loginWithUsername

print("Setting up authentication routes...")
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = {

#         "username": request.form.get('username'),
#         "email": request.form.get('email'),
#         "password": request.form.get('password')
#     }
    
#     return jsonify({"message": "User registered successfully", "data": data}), 201

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
        