"""
Comprehensive test suite for auth_service module to identify bugs
Tests: hashing, verification, login, and edge cases
Uses the actual project Flask app and database
"""
import sys
import uuid
import os
import tempfile

# Create a temporary database file for testing
temp_db_fd, temp_db_path = tempfile.mkstemp()

# Configure environment before importing app
os.environ['FLASK_ENV'] = 'testing'
os.environ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{temp_db_path}'

# Import from the actual project
from app import app, db
from app.db_models import User
from app.auth_service.hashing import hashPassword, checkPasswordHash
from app.auth_service.verification import verifyEmail, verifyPasswordByEmail

class TestAuthService:
    """Test class for auth_service module"""
    
    def __init__(self):
        self.test_cases_passed = 0
        self.test_cases_failed = 0
        self.bugs_found = []
    
    def setup(self):
        """Setup test environment"""
        with app.app_context():
            db.create_all()
            print("✓ Test environment initialized\n")
    
    def teardown(self):
        """Cleanup test environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def create_test_user(self, email, password, name="Test User", role="DONOR"):
        """Create a test user"""
        with app.app_context():
            user = User(
                uid=str(uuid.uuid4()),
                name=name,
                email=email,
                password_hash=hashPassword(password),
                role=role
            )
            db.session.add(user)
            db.session.commit()
            return user
    
    def log_test(self, name, passed, message=""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if message:
            print(f"       {message}")
        
        if passed:
            self.test_cases_passed += 1
        else:
            self.test_cases_failed += 1
            self.bugs_found.append(f"{name} - {message}")
    
    def test_password_hashing(self):
        """Test 1: Password hashing functionality"""
        print("\n" + "="*60)
        print("TEST 1: Password Hashing Functionality")
        print("="*60)
        
        password = "TestPassword123!"
        
        try:
            # Test hashing
            hashed = hashPassword(password)
            is_valid = checkPasswordHash(password, hashed)
            
            self.log_test(
                "Valid password verification",
                is_valid,
                "Password should match after hashing"
            )
            
            # Test wrong password
            is_invalid = checkPasswordHash("WrongPassword", hashed)
            self.log_test(
                "Wrong password rejection",
                not is_invalid,
                "Wrong password should not match"
            )
            
            # Test empty password
            hashed_empty = hashPassword("")
            is_empty_valid = checkPasswordHash("", hashed_empty)
            self.log_test(
                "Empty password handling",
                is_empty_valid,
                "Empty password should work (edge case)"
            )
            
            # Test special characters
            special_password = "P@$$w0rd!#%&*()[]{}|\\:;<>,.?/~`"
            hashed_special = hashPassword(special_password)
            is_special_valid = checkPasswordHash(special_password, hashed_special)
            self.log_test(
                "Special characters in password",
                is_special_valid,
                "Special characters should work"
            )
            
        except Exception as e:
            self.log_test("Password hashing", False, f"Exception: {str(e)}")
    
    def test_email_verification(self):
        """Test 2: Email verification functionality"""
        print("\n" + "="*60)
        print("TEST 2: Email Verification Functionality")
        print("="*60)
        
        with app.app_context():
            try:
                test_email = "verify@example.com"
                self.create_test_user(test_email, "password123")
                
                # Test existing email
                exists = verifyEmail(test_email)
                self.log_test(
                    "Verify existing email",
                    exists,
                    "Should return True for existing email"
                )
                
                # Test non-existent email
                not_exists = verifyEmail("nonexistent@example.com")
                self.log_test(
                    "Verify non-existent email",
                    not not_exists,
                    "Should return False for non-existent email"
                )
                
                # Test None/empty email
                try:
                    result = verifyEmail(None)
                    self.log_test(
                        "Handle None email",
                        result == False,
                        f"Expected False, got {result}"
                    )
                except Exception as e:
                    self.log_test(
                        "Handle None email",
                        False,
                        f"Exception raised: {str(e)}"
                    )
                
                # Test empty string email
                try:
                    result = verifyEmail("")
                    self.log_test(
                        "Handle empty email",
                        result == False,
                        f"Expected False, got {result}"
                    )
                except Exception as e:
                    self.log_test(
                        "Handle empty email",
                        False,
                        f"Exception raised: {str(e)}"
                    )
                
            except Exception as e:
                self.log_test("Email verification", False, f"Exception: {str(e)}")
    
    def test_password_verification_by_email(self):
        """Test 3: Password verification by email"""
        print("\n" + "="*60)
        print("TEST 3: Password Verification by Email")
        print("="*60)
        
        with app.app_context():
            try:
                test_email = "pwd@example.com"
                test_password = "SecurePass123!"
                self.create_test_user(test_email, test_password)
                
                # Test correct password
                is_valid = verifyPasswordByEmail(test_email, test_password)
                self.log_test(
                    "Correct password verification",
                    is_valid,
                    "Should return True for correct password"
                )
                
                # Test wrong password
                is_invalid = verifyPasswordByEmail(test_email, "WrongPassword")
                self.log_test(
                    "Wrong password rejection",
                    not is_invalid,
                    "Should return False for wrong password"
                )
                
                # Test non-existent user
                is_user_invalid = verifyPasswordByEmail("nonexistent@example.com", test_password)
                self.log_test(
                    "Non-existent user rejection",
                    not is_user_invalid,
                    "Should return False for non-existent email"
                )
                
                # Test None email
                result = verifyPasswordByEmail(None, test_password)
                self.log_test(
                    "Handle None email",
                    result == False,
                    "Should return False for None email"
                )
                
                # Test None password
                result = verifyPasswordByEmail(test_email, None)
                self.log_test(
                    "Handle None password",
                    result == False,
                    "Should return False for None password"
                )
                
                # Test empty email
                result = verifyPasswordByEmail("", test_password)
                self.log_test(
                    "Handle empty email",
                    result == False,
                    "Should return False for empty email"
                )
                
                # Test empty password
                result = verifyPasswordByEmail(test_email, "")
                self.log_test(
                    "Handle empty password",
                    result == False,
                    "Should return False for empty password"
                )
                
                # Test both empty
                result = verifyPasswordByEmail("", "")
                self.log_test(
                    "Handle both empty",
                    result == False,
                    "Should return False when both are empty"
                )
                
            except Exception as e:
                self.log_test("Password verification by email", False, f"Exception: {str(e)}")
    
    def test_login_with_email(self):
        """Test 4: Login with email functionality"""
        print("\n" + "="*60)
        print("TEST 4: Login with Email Functionality")
        print("="*60)
        
        with app.app_context():
            try:
                from app.auth_service import loginWithEmail
                
                test_email = "login@example.com"
                test_password = "LoginPass123!"
                user = self.create_test_user(test_email, test_password, name="Login User", role="DONOR")
                
                # Test successful login
                user_data = loginWithEmail(test_email, test_password)
                is_valid_login = user_data is not None and user_data.get('email') == test_email
                self.log_test(
                    "Valid login returns user data",
                    is_valid_login,
                    f"Got: {user_data}"
                )
                
                # Test login returns correct fields
                if user_data:
                    has_uid = 'uid' in user_data
                    has_name = 'name' in user_data
                    has_email = 'email' in user_data
                    has_role = 'role' in user_data
                    
                    all_fields = has_uid and has_name and has_email and has_role
                    self.log_test(
                        "Login returns all required fields",
                        all_fields,
                        f"uid:{has_uid}, name:{has_name}, email:{has_email}, role:{has_role}"
                    )
                
                # Test invalid password
                user_data = loginWithEmail(test_email, "WrongPassword")
                self.log_test(
                    "Invalid password returns None",
                    user_data is None,
                    f"Expected None, got {user_data}"
                )
                
                # Test non-existent user
                user_data = loginWithEmail("nonexistent@example.com", test_password)
                self.log_test(
                    "Non-existent user returns None",
                    user_data is None,
                    f"Expected None, got {user_data}"
                )
                
                # Test None email
                user_data = loginWithEmail(None, test_password)
                self.log_test(
                    "None email returns None",
                    user_data is None,
                    f"Expected None, got {user_data}"
                )
                
                # Test None password
                user_data = loginWithEmail(test_email, None)
                self.log_test(
                    "None password returns None",
                    user_data is None,
                    f"Expected None, got {user_data}"
                )
                
            except ImportError:
                self.log_test("Login with email import", False, "Function not found in __init__.py")
            except Exception as e:
                self.log_test("Login with email", False, f"Exception: {str(e)}")
    
    def test_missing_registration_function(self):
        """Test 5: Check for missing registerUser function"""
        print("\n" + "="*60)
        print("TEST 5: Registration Function Availability")
        print("="*60)
        
        try:
            from app.auth_service import registerUser
            self.log_test(
                "registerUser function exists",
                True,
                "Function is implemented"
            )
        except ImportError:
            self.log_test(
                "registerUser function exists",
                False,
                "BUG FOUND: registerUser is not exported or implemented in __init__.py"
            )
    
    def test_database_null_password_hash(self):
        """Test 6: Handle NULL password_hash from database"""
        print("\n" + "="*60)
        print("TEST 6: Handle NULL/Missing Password Hash")
        print("="*60)
        
        with app.app_context():
            try:
                # Create user with NULL password_hash (simulating DB corruption)
                test_email = "null@example.com"
                user = User(
                    uid=str(uuid.uuid4()),
                    name="Null User",
                    email=test_email,
                    password_hash=None,  # NULL value
                    role="DONOR"
                )
                db.session.add(user)
                db.session.commit()
                
                # Test password verification with NULL hash
                try:
                    result = verifyPasswordByEmail(test_email, "anypassword")
                    self.log_test(
                        "Handle NULL password_hash",
                        result == False,
                        f"Expected False, got {result}"
                    )
                except AttributeError as e:
                    self.log_test(
                        "Handle NULL password_hash",
                        False,
                        f"BUG FOUND: AttributeError raised: {str(e)}"
                    )
                except Exception as e:
                    self.log_test(
                        "Handle NULL password_hash",
                        False,
                        f"Exception raised: {str(e)}"
                    )
                
            except Exception as e:
                self.log_test("NULL password hash test", False, f"Setup exception: {str(e)}")
    
    def test_case_sensitivity(self):
        """Test 7: Email case sensitivity"""
        print("\n" + "="*60)
        print("TEST 7: Email Case Sensitivity")
        print("="*60)
        
        with app.app_context():
            try:
                test_email = "CaseSensitive@Example.COM"
                test_password = "Pass123!"
                self.create_test_user(test_email, test_password)
                
                # Test with different cases
                from app.auth_service import loginWithEmail
                
                # Exact case
                result1 = loginWithEmail(test_email, test_password)
                is_exact = result1 is not None
                self.log_test(
                    "Login with exact case",
                    is_exact,
                    "Should succeed with exact case"
                )
                
                # Different case
                result2 = loginWithEmail(test_email.lower(), test_password)
                is_lower = result2 is not None
                self.log_test(
                    "Login with lowercase email",
                    is_lower,
                    f"Expected success, got {'success' if is_lower else 'failure'} - DB column is case-sensitive"
                )
                
            except Exception as e:
                self.log_test("Case sensitivity", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("SURPLUSX AUTH_SERVICE BUG TEST SUITE")
        print("="*60)
        
        self.setup()
        
        self.test_password_hashing()
        self.test_email_verification()
        self.test_password_verification_by_email()
        self.test_login_with_email()
        self.test_missing_registration_function()
        self.test_database_null_password_hash()
        self.test_case_sensitivity()
        
        self.teardown()
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"✓ Passed: {self.test_cases_passed}")
        print(f"✗ Failed: {self.test_cases_failed}")
        print(f"Total:   {self.test_cases_passed + self.test_cases_failed}")
        
        if self.bugs_found:
            print("\n" + "="*60)
            print("🐛 BUGS FOUND:")
            print("="*60)
            for i, bug in enumerate(self.bugs_found, 1):
                print(f"{i}. {bug}")
        else:
            print("\n✓ No bugs found!")
        
        print("\n" + "="*60)
        
        return self.test_cases_failed == 0

if __name__ == "__main__":
    tester = TestAuthService()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
