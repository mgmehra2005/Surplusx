from app import app
from flask import request, jsonify

print("Setting up authentication routes...")
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = {
        "username": request.form.get('username'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
    }
    
    return jsonify({"message": "User registered successfully", "data": data}), 201