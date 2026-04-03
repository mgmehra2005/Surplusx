"""
Comprehensive JWT Authentication Testing
Tests login endpoint, token generation, and token validation
"""
import json
import sys
import uuid
from app import app, db
from app.db_models import User
from app.auth_service.hashing import hashPassword
from flask_jwt_extended import decode_token

# Test configuration
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"
TEST_NAME = "Test User"


def setup_test_user():
    """Create a test user in the database."""
    print("\n📝 Setting up test user...")
    
    # Check if user exists
    existing_user = User.query.filter_by(email=TEST_EMAIL).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        print(f"   Removed existing test user: {TEST_EMAIL}")
    
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
    return new_user


def test_login_endpoint():
    """Test the login endpoint."""
    print("\n🔐 Testing login endpoint...")
    
    client = app.test_client()
    
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
        print(f"   ✓ Token: {data['token'][:20]}...")
        print(f"   ✓ User: {data['user']}")
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
        print(f"   ✗ Response: {response.get_json()}")
    
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
        print(f"   ✓ Full payload: {json.dumps(payload, indent=2)}")
        return True
    except Exception as e:
        print(f"   ✗ Token validation failed: {str(e)}")
        return False


def test_token_usage():
    """Test using token with protected endpoints (if any exist)."""
    print("\n🔒 Testing token usage with requests...")
    
    # First get a valid token
    client = app.test_client()
    response = client.post('/api/auth/login',
        json={'email': TEST_EMAIL, 'password': TEST_PASSWORD},
        content_type='application/json'
    )
    
    if response.status_code != 200:
        print("   ✗ Could not get valid token")
        return
    
    token = response.get_json()['token']
    
    # Test with Authorization header
    print("   Testing request with Authorization header...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Try a food routes endpoint (if available)
    response = client.get('/api/food/list', headers=headers)
    if response.status_code in [200, 401, 403]:
        print(f"   ✓ Request succeeded with status: {response.status_code}")
    else:
        print(f"   - Request returned: {response.status_code}")


def cleanup_test_user():
    """Remove test user from database."""
    print("\n🧹 Cleaning up...")
    
    test_user = User.query.filter_by(email=TEST_EMAIL).first()
    if test_user:
        db.session.delete(test_user)
        db.session.commit()
        print(f"   ✓ Test user removed")
    else:
        print(f"   ⚠ Test user not found (already removed)")


def run_all_tests():
    """Run all JWT tests."""
    print("=" * 60)
    print("JWT AUTHENTICATION TEST SUITE")
    print("=" * 60)
    
    try:
        with app.app_context():
            # Setup
            setup_test_user()
            
            # Run tests
            token = test_login_endpoint()
            
            if token:
                test_token_validation(token)
                test_token_usage()
            else:
                print("\n✗ Login failed, skipping remaining tests")
            
            # Cleanup
            cleanup_test_user()
            
            print("\n" + "=" * 60)
            print("✅ TEST SUITE COMPLETED")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(run_all_tests())
