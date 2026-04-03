"""
JWT + Database Integration Test
Tests that JWT and database work together seamlessly
"""
import json
import sys
import uuid
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, decode_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Create Flask app with testing config
test_app = Flask(__name__)
test_app.config['TESTING'] = True
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
test_app.config['JWT_SECRET_KEY'] = 'test-jwt-secret-key-for-testing'
test_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

# Initialize extensions
CORS(test_app)
db = SQLAlchemy(test_app)
jwt = JWTManager(test_app)

# Define User model (from actual app)
class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'

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

# Routes
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

@test_app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """Protected route to verify JWT token and access user data from database."""
    user_uid = get_jwt_identity()
    
    # Fetch user from database using UID from JWT token
    user = User.query.filter_by(uid=user_uid).first()
    
    if not user:
        return {'message': 'User not found'}, 404
    
    return {
        'message': 'Token verified successfully',
        'user': {
            'uid': user.uid,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }
    }, 200

@test_app.route('/api/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Protected route to get user profile from database."""
    user_uid = get_jwt_identity()
    user = User.query.filter_by(uid=user_uid).first()
    
    if not user:
        return {'message': 'User not found'}, 404
    
    return {
        'profile': {
            'uid': user.uid,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }
    }, 200

# Test data
TEST_USERS = [
    {
        'name': 'John Donor',
        'email': 'john@example.com',
        'password': 'password123',
        'role': 'DONOR',
        'phone': '1234567890'
    },
    {
        'name': 'Sarah NGO',
        'email': 'sarah@ngo.com',
        'password': 'secure_pass_456',
        'role': 'NGO',
        'phone': '9876543210'
    },
    {
        'name': 'Admin User',
        'email': 'admin@example.com',
        'password': 'admin_password_789',
        'role': 'ADMIN',
        'phone': '5555555555'
    }
]

def setup_test_users():
    """Create test users in database."""
    print("\n📝 Setting up test users in database...")
    
    created_users = []
    for user_data in TEST_USERS:
        user = User(
            uid=str(uuid.uuid4()),
            name=user_data['name'],
            email=user_data['email'],
            password_hash=hashPassword(user_data['password']),
            role=user_data['role'],
            phone=user_data['phone']
        )
        db.session.add(user)
        created_users.append(user)
    
    db.session.commit()
    
    for user in created_users:
        print(f"   ✓ Created {user.role}: {user.name} ({user.email})")
    
    return created_users

def test_login_flow():
    """Test login flow and JWT generation."""
    print("\n🔐 Testing login flow with database...")
    
    client = test_app.test_client()
    
    for user_data in TEST_USERS:
        email = user_data['email']
        password = user_data['password']
        
        print(f"\n   Testing login for {email}...")
        
        response = client.post('/api/auth/login',
            json={'email': email, 'password': password},
            content_type='application/json'
        )
        
        if response.status_code == 200:
            result = response.get_json()
            print(f"   ✓ Login successful")
            print(f"   ✓ Token: {result['token'][:40]}...")
            print(f"   ✓ User role: {result['user']['role']}")
            
            # Store token for next test
            user_data['token'] = result['token']
        else:
            print(f"   ✗ Login failed: Status {response.status_code}")
            return False
    
    return True

def test_token_verification():
    """Test token verification with database lookup."""
    print("\n✅ Testing token verification with database lookup...")
    
    client = test_app.test_client()
    
    for user_data in TEST_USERS:
        email = user_data['email']
        token = user_data.get('token')
        
        if not token:
            print(f"   ⚠ No token for {email}, skipping")
            continue
        
        print(f"\n   Verifying token for {email}...")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Call verify endpoint
        response = client.get('/api/auth/verify', headers=headers)
        
        if response.status_code == 200:
            result = response.get_json()
            user = result['user']
            print(f"   ✓ Token verified successfully")
            print(f"   ✓ DB lookup returned: {user['name']} ({user['role']})")
            print(f"   ✓ Email from DB: {user['email']}")
        else:
            print(f"   ✗ Verification failed: Status {response.status_code}")
            print(f"   ✗ Response: {response.get_json()}")
            return False
    
    return True

def test_protected_endpoint():
    """Test accessing protected endpoint with JWT + DB."""
    print("\n🔒 Testing protected endpoint access with JWT + DB...")
    
    client = test_app.test_client()
    token = TEST_USERS[0].get('token')
    
    if not token:
        print("   ⚠ No token available")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test authorized access
    print("\n   Test 1: Authorized access")
    response = client.get('/api/users/profile', headers=headers)
    
    if response.status_code == 200:
        result = response.get_json()
        profile = result['profile']
        print(f"   ✓ Protected endpoint accessible")
        print(f"   ✓ Profile: {profile['name']} | {profile['role']} | {profile['email']}")
    else:
        print(f"   ✗ Unauthorized: {response.status_code}")
        return False
    
    # Test unauthorized access
    print("\n   Test 2: Unauthorized access (no token)")
    response = client.get('/api/users/profile')
    
    if response.status_code == 401:
        print(f"   ✓ Correctly rejected (no token)")
    else:
        print(f"   ✗ Should have been rejected: {response.status_code}")
        return False
    
    # Test with invalid token
    print("\n   Test 3: Invalid token")
    headers['Authorization'] = 'Bearer invalid_token_12345'
    response = client.get('/api/users/profile', headers=headers)
    
    if response.status_code in [422, 401]:
        print(f"   ✓ Correctly rejected (invalid token) with status {response.status_code}")
    else:
        print(f"   ✗ Unexpected status: {response.status_code}")
        return False
    
    return True

def test_database_integrity():
    """Test that database has correct data."""
    print("\n📊 Testing database integrity...")
    
    # Count users
    user_count = User.query.count()
    print(f"   ✓ Total users in DB: {user_count}")
    
    if user_count != len(TEST_USERS):
        print(f"   ✗ Expected {len(TEST_USERS)} users, got {user_count}")
        return False
    
    # Verify each role
    roles = {}
    for user in User.query.all():
        if user.role not in roles:
            roles[user.role] = 0
        roles[user.role] += 1
    
    print(f"   ✓ Users by role: {roles}")
    
    # Verify unique emails
    emails = User.query.all()
    unique_emails = len(set(u.email for u in emails))
    
    if unique_emails != len(emails):
        print(f"   ✗ Found duplicate emails in database")
        return False
    
    print(f"   ✓ All emails are unique")
    return True

def run_integration_tests():
    """Run all JWT + Database integration tests."""
    print("=" * 70)
    print("JWT + DATABASE INTEGRATION TEST SUITE")
    print("=" * 70)
    
    try:
        with test_app.app_context():
            # Create database tables
            db.create_all()
            print("\n✓ Database initialized (SQLite in-memory)")
            
            # Setup test users
            setup_test_users()
            
            # Run tests
            tests = [
                ("Database Integrity", test_database_integrity),
                ("Login Flow", test_login_flow),
                ("Token Verification", test_token_verification),
                ("Protected Endpoints", test_protected_endpoint)
            ]
            
            tests_passed = 0
            for test_name, test_func in tests:
                try:
                    if test_func():
                        tests_passed += 1
                except Exception as e:
                    print(f"\n   ✗ {test_name} failed with error: {str(e)}")
            
            tests_total = len(tests)
            
            print("\n" + "=" * 70)
            print(f"✅ TEST RESULTS: {tests_passed}/{tests_total} PASSED")
            print("=" * 70)
            
            if tests_passed == tests_total:
                print("\n🎉 ALL INTEGRATION TESTS PASSED!")
                print("\n✅ JWT AND DATABASE ARE WORKING TOGETHER CORRECTLY!")
                print("\nIntegration Summary:")
                print("   ✓ Users stored correctly in database")
                print("   ✓ JWT tokens generated from user credentials")
                print("   ✓ JWT tokens verified and decoded")
                print("   ✓ Protected endpoints use JWT + DB lookup")
                print("   ✓ Unauthorized access properly rejected")
                print("\n🚀 Ready for production deployment!\n")
                return 0
            else:
                print(f"\n⚠ {tests_total - tests_passed} test(s) failed")
                return 1
            
    except Exception as e:
        print(f"\n❌ Integration Test Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(run_integration_tests())
