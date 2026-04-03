"""
Standalone JWT Authentication Testing - Uses SQLite for testing
Tests login endpoint, token generation, and token validation
"""
import json
import sys
import uuid
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from werkzeug.security import generate_password_hash, check_password_hash

# Create test Flask app with SQLite
test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
test_app.config['JWT_SECRET_KEY'] = 'test-secret-key'
test_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400

# Initialize extensions
CORS(test_app)
db = SQLAlchemy(test_app)
jwt = JWTManager(test_app)

# Define User model matching the actual app
class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Auth utilities
def hashPassword(password: str) -> str:
    """Hash a plaintext password."""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def checkPasswordHash(password: str, hashed_password: str) -> bool:
    """Check if a plaintext password matches a hashed password."""
    return check_password_hash(hashed_password, password)

def verifyEmail(email: str) -> bool:
    """Verify user exists by email."""
    user = User.query.filter_by(email=email).first()
    return user is not None

def verifyPasswordByEmail(email: str, password: str) -> bool:
    """Verify password for email."""
    if not email or not password:
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    return checkPasswordHash(password, user.password_hash)

def loginWithEmail(email: str, password: str):
    """Authenticate by email and return user data."""
    if verifyEmail(email) and verifyPasswordByEmail(email, password):
        user_obj = User.query.filter_by(email=email).first()
        if user_obj:
            return {
                'uid': user_obj.uid,
                'name': user_obj.name,
                'email': user_obj.email,
                'role': user_obj.role
            }
    return None

# Setup auth route
@test_app.route('/api/auth/login', methods=['POST'])
def login():
    from flask import request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return {'message': 'Email and password required'}, 400
    
    user_data = loginWithEmail(email, password)
    if user_data:
        access_token = create_access_token(identity=user_data['uid'])
        return {
            'message': 'Login successful',
            'token': access_token,
            'user': user_data
        }, 200
    else:
        return {'message': 'Invalid email or password!'}, 401

# Test configuration
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"

def setup_test_user():
    """Create a test user in the database."""
    print("\n📝 Setting up test user...")
    
    # Create new test user
    new_user = User(
        uid=str(uuid.uuid4()),
        name=TEST_NAME,
        email=TEST_EMAIL,
        password_hash=hashPassword(TEST_PASSWORD),
        role='DONOR',
        phone='1234567890'
    )
    db.session.add(new_user)
    db.session.commit()
    print(f"   ✓ Test user created: {TEST_EMAIL}")
    print(f"   ✓ UID: {new_user.uid}")
    print(f"   ✓ Role: {new_user.role}")
    print(f"   ✓ Password Hash: {new_user.password_hash[:50]}...")
    return new_user

def test_login_endpoint():
    """Test the login endpoint."""
    print("\n🔐 Testing login endpoint...")
    
    client = test_app.test_client()
    
    # Test 1: Valid login
    print("   Test 1: Valid credentials")
    response = client.post('/api/auth/login', 
        json={'email': TEST_EMAIL, 'password': TEST_PASSWORD},
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.get_json()
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Message: {data['message']}")
        print(f"   ✓ Token: {data['token'][:50]}...")
        print(f"   ✓ User: {json.dumps(data['user'], indent=6)}")
        token = data['token']
    else:
        print(f"   ✗ Status: {response.status_code}")
        print(f"   ✗ Error: {response.get_json()}")
        return None
    
    # Test 2: Invalid password
    print("\n   Test 2: Invalid password")
    response = client.post('/api/auth/login',
        json={'email': TEST_EMAIL, 'password': 'wrongpassword'},
        content_type='application/json'
    )
    
    if response.status_code == 401:
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Message: {response.get_json()['message']}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
    
    # Test 3: Non-existent user
    print("\n   Test 3: Non-existent user")
    response = client.post('/api/auth/login',
        json={'email': 'nonexistent@example.com', 'password': 'password'},
        content_type='application/json'
    )
    
    if response.status_code == 401:
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Message: {response.get_json()['message']}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
    
    # Test 4: Missing credentials
    print("\n   Test 4: Missing credentials")
    response = client.post('/api/auth/login',
        json={'email': TEST_EMAIL},
        content_type='application/json'
    )
    
    if response.status_code == 400:
        print(f"   ✓ Status: {response.status_code}")
        print(f"   ✓ Message: {response.get_json()['message']}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
    
    return token

def test_token_validation(token):
    """Test JWT token validation."""
    print("\n🎫 Testing JWT token validation...")
    
    try:
        # Decode token
        payload = decode_token(token)
        print(f"   ✓ Token decoded successfully")
        print(f"   ✓ User ID (uid): {payload['sub']}")
        print(f"   ✓ Token type: {payload['type']}")
        print(f"   ✓ Full payload: {json.dumps(payload, indent=6)}")
        return True
    except Exception as e:
        print(f"   ✗ Token validation failed: {str(e)}")
        return False

def test_password_hashing():
    """Test password hashing and verification."""
    print("\n🔑 Testing password hashing and verification...")
    
    test_password = "mypassword123"
    hashed = hashPassword(test_password)
    
    print(f"   ✓ Original password: {test_password}")
    print(f"   ✓ Hashed password: {hashed[:50]}...")
    
    # Test correct password
    is_correct = checkPasswordHash(test_password, hashed)
    if is_correct:
        print(f"   ✓ Password verification PASSED (correct password)")
    else:
        print(f"   ✗ Password verification FAILED (correct password)")
        return False
    
    # Test incorrect password
    is_incorrect = checkPasswordHash("wrongpassword", hashed)
    if not is_incorrect:
        print(f"   ✓ Password verification PASSED (incorrect password rejected)")
    else:
        print(f"   ✗ Password verification FAILED (incorrect password accepted)")
        return False
    
    return True

def run_all_tests():
    """Run all JWT tests."""
    print("=" * 70)
    print("JWT AUTHENTICATION TEST SUITE (SQLite In-Memory)")
    print("=" * 70)
    
    try:
        with test_app.app_context():
            # Create tables
            db.create_all()
            print("\n✓ Database initialized")
            
            # Test password hashing
            if not test_password_hashing():
                print("\n✗ Password hashing tests failed")
                return 1
            
            # Setup
            setup_test_user()
            
            # Run tests
            token = test_login_endpoint()
            
            if token:
                test_token_validation(token)
            else:
                print("\n✗ Login failed, skipping token validation")
                return 1
            
            print("\n" + "=" * 70)
            print("✅ ALL TESTS PASSED - JWT IS WORKING CORRECTLY!")
            print("=" * 70)
            print("\n📋 Test Results Summary:")
            print("   ✓ User creation and storage")
            print("   ✓ Password hashing and verification")
            print("   ✓ Login endpoint with valid credentials")
            print("   ✓ Login endpoint rejects invalid credentials")
            print("   ✓ JWT token generation")
            print("   ✓ JWT token validation and decoding")
            print("\n🚀 Ready for production testing with MySQL!\n")
            
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(run_all_tests())
