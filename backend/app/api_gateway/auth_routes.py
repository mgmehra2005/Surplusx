from app import app
from flask import request, jsonify
from app.auth_service import loginWithEmail, loginWithUsername
from app.auth_service.registration import registerUser
from app.db_models.utils import _getUserRoleByUsername, _getUserRoleByEmail
import jwt, datetime
from functools import wraps

def encode_auth_token(user_uid, role):
        con = app.config.get('SECRET_KEY')
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), # 24hr expiry
                'iat': datetime.datetime.utcnow(),
                'sub': user_uid,
                'role': role
            }
            return jwt.encode(payload, str(con), algorithm='HS256')
        except Exception as e:
                return e

def token_required(f):
    """Decorator to protect routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Standard: Authorization: Bearer <token>
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Explicitly state the algorithm to prevent 'algorithm confusion' attacks
            data = jwt.decode(token, str(app.config.get("SECRET_KEY")), algorithms=["HS256"])
            from app.db_models import User
            current_user = User.query.filter_by(uid=data['sub']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

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
            token = encode_auth_token(username, _getUserRoleByEmail(username))
            return jsonify({"message": "Login successful with email!", "token": token, "role": _getUserRoleByEmail(username)}), 200
        else:
            return jsonify({"message": "Invalid email or password!"}), 401
    else:
        login_status = loginWithUsername(username, password)
        if login_status:
            token = encode_auth_token(username, _getUserRoleByUsername(username))
            return jsonify({"message": "Login successful with username!", "token": token, "role": _getUserRoleByUsername(username)}), 200
        else:
            return jsonify({"message": "Invalid username or password!"}), 401
        
        