#!/usr/bin/env python3
"""
Comprehensive test for all audit fixes implementation
Tests critical security and performance improvements
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path.parent))

def test_imports():
    """Test all critical imports work."""
    print("🧪 Test 1: Checking imports...")
    try:
        from app import app, db
        from app.utils import (
            normalize_email,
            validate_email_format,
            validate_password_strength,
            sanitize_input
        )
        from app.auth_service import loginWithEmail, registerUser
        from config import Config, DevelopmentConfig, ProductionConfig
        print("   ✅ All imports successful")
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False


def test_email_normalization():
    """Test email normalization for case-insensitive comparison."""
    print("\n🧪 Test 2: Email normalization...")
    try:
        from app.utils import normalize_email
        
        test_cases = [
            ("TEST@EXAMPLE.COM", "test@example.com"),
            ("Test@Example.Com", "test@example.com"),
            ("test@example.com", "test@example.com"),
            ("  TEST@EXAMPLE.COM  ", "test@example.com"),
        ]
        
        for input_email, expected in test_cases:
            result = normalize_email(input_email)
            assert result == expected, f"Expected {expected}, got {result}"
        
        print("   ✅ Email normalization working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Email normalization failed: {e}")
        return False


def test_email_validation():
    """Test email format validation."""
    print("\n🧪 Test 3: Email format validation...")
    try:
        from app.utils import validate_email_format
        
        valid_emails = [
            "user@example.com",
            "test.user@example.co.uk",
            "user+tag@example.com",
        ]
        
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user @example.com",
        ]
        
        for email in valid_emails:
            assert validate_email_format(email), f"Should validate {email}"
        
        for email in invalid_emails:
            assert not validate_email_format(email), f"Should not validate {email}"
        
        print("   ✅ Email validation working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Email validation failed: {e}")
        return False


def test_password_strength():
    """Test password strength validation."""
    print("\n🧪 Test 4: Password strength validation...")
    try:
        from app.utils import validate_password_strength
        
        # Valid passwords (must have: upper, lower, digit, special, 8+ chars)
        valid_passwords = [
            "MyPass123!",
            "Secure@Pass1",
            "Str0ng#Pwd",
        ]
        
        # Invalid passwords
        invalid_passwords = [
            "short",           # Too short
            "nouppercase123!",  # Missing uppercase
            "NOLOWERCASE123!",  # Missing lowercase
            "NoDigitHere!",     # Missing digit
            "Nospecial123",     # Missing special character
        ]
        
        for pwd in valid_passwords:
            is_valid, msg = validate_password_strength(pwd)
            assert is_valid, f"Password '{pwd}' should be valid: {msg}"
        
        for pwd in invalid_passwords:
            is_valid, msg = validate_password_strength(pwd)
            assert not is_valid, f"Password '{pwd}' should be invalid"
        
        print("   ✅ Password strength validation working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Password strength validation failed: {e}")
        return False


def test_input_sanitization():
    """Test input sanitization for security."""
    print("\n🧪 Test 5: Input sanitization...")
    try:
        from app.utils import sanitize_input
        
        # Test dangerous characters are removed
        dangerous_input = '<script>alert("xss")</script>'
        result = sanitize_input(dangerous_input)
        
        # Should not contain < > or " which are dangerous
        assert '<' not in result, "Dangerous < character not removed"
        assert '>' not in result, "Dangerous > character not removed"
        
        # Test normal input is preserved
        normal_input = 'John Doe'
        result = sanitize_input(normal_input)
        assert 'John' in result and 'Doe' in result, "Normal text should be preserved"
        
        print("   ✅ Input sanitization working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Input sanitization failed: {e}")
        return False


def test_config_setup():
    """Test configuration setup with security improvements."""
    print("\n🧪 Test 6: Configuration setup...")
    try:
        from config import Config, DevelopmentConfig
        
        # Check that config has required security settings
        assert hasattr(Config, 'MAX_CONTENT_LENGTH'), "Missing MAX_CONTENT_LENGTH"
        assert hasattr(Config, 'SQLALCHEMY_ENGINE_OPTIONS'), "Missing SQLALCHEMY_ENGINE_OPTIONS"
        assert hasattr(Config, 'SESSION_COOKIE_HTTPONLY'), "Missing SESSION_COOKIE_HTTPONLY"
        
        # Check values
        assert Config.MAX_CONTENT_LENGTH == 10 * 1024 * 1024, "MAX_CONTENT_LENGTH should be 10MB"
        assert Config.SESSION_COOKIE_HTTPONLY == True, "SESSION_COOKIE_HTTPONLY should be True"
        
        # Check connection pooling
        engine_opts = Config.SQLALCHEMY_ENGINE_OPTIONS
        assert 'pool_size' in engine_opts, "Missing pool_size setting"
        assert 'max_overflow' in engine_opts, "Missing max_overflow setting"
        assert 'pool_pre_ping' in engine_opts, "Missing pool_pre_ping setting"
        
        print("   ✅ Configuration setup correct with all security settings")
        return True
    except Exception as e:
        print(f"   ❌ Configuration setup failed: {e}")
        return False


def test_database_models():
    """Test database models have indexes added."""
    print("\n🧪 Test 7: Database models and indexes...")
    try:
        from app import db
        from app.db_models import User, FoodListing
        
        # Check User model has indexes
        user_indexes = [idx.name for idx in User.__table__.indexes]
        assert any('email' in idx for idx in user_indexes), "User should have email index"
        assert any('role' in idx for idx in user_indexes), "User should have role index"
        
        # Check FoodListing model has indexes
        food_indexes = [idx.name for idx in FoodListing.__table__.indexes]
        assert any('status' in idx for idx in food_indexes), "FoodListing should have status index"
        assert any('donor' in idx for idx in food_indexes), "FoodListing should have donor index"
        assert any('expiry' in idx for idx in food_indexes), "FoodListing should have expiry index"
        
        print("   ✅ Database models have proper indexes for performance")
        return True
    except Exception as e:
        print(f"   ❌ Database models check failed: {e}")
        return False


def test_health_check_endpoint():
    """Test health check endpoint exists."""
    print("\n🧪 Test 8: Health check endpoint...")
    try:
        from app import app
        
        # Check that health check route is registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        assert any('/health' in route for route in routes), "Health check endpoint not found"
        
        print("   ✅ Health check endpoint registered")
        return True
    except Exception as e:
        print(f"   ❌ Health check endpoint check failed: {e}")
        return False


def test_auth_routes_logging():
    """Test that auth routes have logging configured."""
    print("\n🧪 Test 9: Auth routes logging...")
    try:
        import inspect
        from app.api_gateway import auth_routes
        
        source = inspect.getsource(auth_routes)
        
        # Check for logging
        assert 'import logging' in source, "logging module not imported"
        assert 'logger = logging' in source, "logger not initialized"
        assert 'logger.error' in source or 'logger.info' in source, "logger not used"
        
        # Check that print statements are removed or minimized
        assert source.count('print(') < 2, "Too many print statements (should use logging)"
        
        print("   ✅ Auth routes have proper logging")
        return True
    except Exception as e:
        print(f"   ❌ Auth routes logging check failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🔒 AUDIT FIXES VERIFICATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_email_normalization,
        test_email_validation,
        test_password_strength,
        test_input_sanitization,
        test_config_setup,
        test_database_models,
        test_health_check_endpoint,
        test_auth_routes_logging,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"Unexpected error in {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ ALL AUDIT FIXES VERIFIED - SYSTEM READY")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - CHECK OUTPUT ABOVE")
        return 1


if __name__ == '__main__':
    sys.exit(main())
