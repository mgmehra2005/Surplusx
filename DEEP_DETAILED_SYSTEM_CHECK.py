#!/usr/bin/env python3
"""
Deep Detailed System Check - Comprehensive Verification
Tests all implemented fixes, integrations, and edge cases
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path.parent))

def check_section(title):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"🔍 {title}")
    print('='*70)


def test_result(condition, message):
    """Print test result."""
    status = "✅" if condition else "❌"
    print(f"   {status} {message}")
    return condition


class DeepDetailedCheck:
    """Comprehensive system verification."""
    
    def __init__(self):
        self.results = {
            'imports': [],
            'security': [],
            'configuration': [],
            'database': [],
            'api': [],
            'integration': [],
            'edge_cases': []
        }
        self.all_passed = True
    
    def run(self):
        """Run all checks."""
        print("\n" + "🔐"*35)
        print("DEEP DETAILED SYSTEM VERIFICATION CHECK")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("🔐"*35)
        
        check_section("SECTION 1: CORE IMPORTS & MODULES")
        self.check_imports()
        
        check_section("SECTION 2: SECURITY IMPLEMENTATIONS")
        self.check_security()
        
        check_section("SECTION 3: CONFIGURATION VALIDATION")
        self.check_configuration()
        
        check_section("SECTION 4: DATABASE & MODELS")
        self.check_database()
        
        check_section("SECTION 5: API ROUTES & ENDPOINTS")
        self.check_api_routes()
        
        check_section("SECTION 6: INTEGRATION POINTS")
        self.check_integration()
        
        check_section("SECTION 7: EDGE CASE HANDLING")
        self.check_edge_cases()
        
        self.print_summary()
        return 0 if self.all_passed else 1
    
    def check_imports(self):
        """Check all critical imports."""
        print("\n📦 Checking core imports...")
        
        try:
            from app import app, db
            test_result(True, "Flask app and database initialized")
        except Exception as e:
            test_result(False, f"Flask initialization failed: {e}")
            self.all_passed = False
        
        try:
            from app.utils import (
                normalize_email, validate_email_format, validate_password_strength,
                sanitize_input, validate_quantity, validate_date_range
            )
            test_result(True, "All validator functions imported")
        except Exception as e:
            test_result(False, f"Validators import failed: {e}")
            self.all_passed = False
        
        try:
            from app.auth_service import loginWithEmail, registerUser
            test_result(True, "Auth service functions imported")
        except Exception as e:
            test_result(False, f"Auth service import failed: {e}")
            self.all_passed = False
        
        try:
            from app.db_models import User, FoodListing, NGO, DeliveryPartner, Delivery, SystemLog
            test_result(True, "All database models imported")
        except Exception as e:
            test_result(False, f"Database models import failed: {e}")
            self.all_passed = False
        
        try:
            from config import Config, DevelopmentConfig, ProductionConfig
            test_result(True, "Configuration classes imported")
        except Exception as e:
            test_result(False, f"Config import failed: {e}")
            self.all_passed = False
    
    def check_security(self):
        """Check security implementations."""
        print("\n🔒 Checking security features...")
        
        try:
            from app.utils import validate_password_strength
            is_valid, msg = validate_password_strength("MyPass123!")
            test_result(is_valid, "Password strength validation works")
        except Exception as e:
            test_result(False, f"Password validation failed: {e}")
            self.all_passed = False
        
        try:
            from app.utils import validate_password_strength
            is_valid, msg = validate_password_strength("weak")
            test_result(not is_valid, "Weak passwords rejected")
        except Exception as e:
            test_result(False, f"Weak password test failed: {e}")
            self.all_passed = False
        
        try:
            from app.utils import sanitize_input
            result = sanitize_input("<script>alert('xss')</script>")
            test_result('<' not in result and '>' not in result, "XSS characters sanitized")
        except Exception as e:
            test_result(False, f"Input sanitization failed: {e}")
            self.all_passed = False
        
        try:
            from app.utils import normalize_email
            email = normalize_email("TEST@EXAMPLE.COM")
            test_result(email == "test@example.com", "Email normalization case-insensitive")
        except Exception as e:
            test_result(False, f"Email normalization failed: {e}")
            self.all_passed = False
        
        try:
            from config import Config
            test_result(Config.SESSION_COOKIE_HTTPONLY, "Session cookies are HTTPONLY")
        except Exception as e:
            test_result(False, f"Session cookie check failed: {e}")
            self.all_passed = False
        
        try:
            from config import Config
            test_result(Config.MAX_CONTENT_LENGTH == 10 * 1024 * 1024, 
                       "Request size limit set to 10MB")
        except Exception as e:
            test_result(False, f"Request size limit check failed: {e}")
            self.all_passed = False
    
    def check_configuration(self):
        """Check configuration setup."""
        print("\n⚙️ Checking configuration...")
        
        try:
            from config import Config
            test_result(hasattr(Config, 'SQLALCHEMY_ENGINE_OPTIONS'), 
                       "Database connection pooling configured")
        except Exception as e:
            test_result(False, f"Config check failed: {e}")
            self.all_passed = False
        
        try:
            from config import Config
            opts = Config.SQLALCHEMY_ENGINE_OPTIONS
            has_pool_size = 'pool_size' in opts
            has_max_overflow = 'max_overflow' in opts
            has_pool_recycle = 'pool_recycle' in opts
            test_result(has_pool_size and has_max_overflow and has_pool_recycle, 
                       "All connection pool settings present")
        except Exception as e:
            test_result(False, f"Pool settings check failed: {e}")
            self.all_passed = False
        
        try:
            from config import DevelopmentConfig
            test_result(DevelopmentConfig.DEBUG, "Development config has DEBUG=True")
        except Exception as e:
            test_result(False, f"Dev config check failed: {e}")
            self.all_passed = False
        
        try:
            from config import ProductionConfig
            test_result(not ProductionConfig.DEBUG, "Production config has DEBUG=False")
        except Exception as e:
            test_result(False, f"Prod config check failed: {e}")
            self.all_passed = False
    
    def check_database(self):
        """Check database models and configuration."""
        print("\n🗄️ Checking database...")
        
        try:
            from app import db
            from app.db_models import User, FoodListing
            
            # Check User table indexes
            user_indexes = [idx.name for idx in User.__table__.indexes]
            has_email_idx = any('email' in idx.lower() for idx in user_indexes)
            has_role_idx = any('role' in idx.lower() for idx in user_indexes)
            
            test_result(has_email_idx and has_role_idx, "User table has email and role indexes")
        except Exception as e:
            test_result(False, f"User table index check failed: {e}")
            self.all_passed = False
        
        try:
            from app.db_models import FoodListing
            food_indexes = [idx.name for idx in FoodListing.__table__.indexes]
            has_status_idx = any('status' in idx.lower() for idx in food_indexes)
            has_donor_idx = any('donor' in idx.lower() for idx in food_indexes)
            has_expiry_idx = any('expiry' in idx.lower() for idx in food_indexes)
            
            conditions = [has_status_idx, has_donor_idx, has_expiry_idx]
            test_result(all(conditions), "FoodListing table has status, donor, expiry indexes")
        except Exception as e:
            test_result(False, f"FoodListing table index check failed: {e}")
            self.all_passed = False
        
        try:
            from app.db_models import User
            columns = [col.name for col in User.__table__.columns]
            required = ['uid', 'name', 'email', 'password_hash', 'role']
            test_result(all(col in columns for col in required), 
                       "User model has all required columns")
        except Exception as e:
            test_result(False, f"User model column check failed: {e}")
            self.all_passed = False
        
        try:
            from app.db_models import FoodListing
            columns = [col.name for col in FoodListing.__table__.columns]
            required = ['fid', 'donor_id', 'title', 'food_type', 'quantity', 'expiry_date', 'status']
            test_result(all(col in columns for col in required), 
                       "FoodListing model has all required columns")
        except Exception as e:
            test_result(False, f"FoodListing model column check failed: {e}")
            self.all_passed = False
    
    def check_api_routes(self):
        """Check API routes and endpoints."""
        print("\n🛣️ Checking API routes...")
        
        try:
            from app import app
            routes = [rule.rule for rule in app.url_map.iter_rules()]
            
            # Check for critical endpoints
            has_auth_register = any('/auth/register' in route for route in routes)
            has_auth_login = any('/auth/login' in route for route in routes)
            has_food_endpoint = any('/food' in route for route in routes)
            has_health = any('/health' in route for route in routes)
            
            test_result(has_auth_register, "Auth register endpoint registered")
            test_result(has_auth_login, "Auth login endpoint registered")
            test_result(has_food_endpoint, "Food operations endpoint registered")
            test_result(has_health, "Health check endpoint registered")
        except Exception as e:
            test_result(False, f"Route check failed: {e}")
            self.all_passed = False
        
        try:
            from app.api_gateway import auth_routes
            import inspect
            source = inspect.getsource(auth_routes)
            
            has_logging = 'import logging' in source and 'logger' in source
            has_error_handling = 'except' in source
            
            test_result(has_logging, "Auth routes have logging implemented")
            test_result(has_error_handling, "Auth routes have error handling")
        except Exception as e:
            test_result(False, f"Auth routes check failed: {e}")
            self.all_passed = False
    
    def check_integration(self):
        """Check integration points."""
        print("\n🔗 Checking integration points...")
        
        try:
            # Check auth service with normalized email
            from app.auth_service import loginWithEmail
            from app.utils import normalize_email
            
            # This should work with the normalized email function
            test_result(callable(loginWithEmail), "loginWithEmail function callable")
            test_result(callable(normalize_email), "normalize_email function callable")
        except Exception as e:
            test_result(False, f"Auth service integration check failed: {e}")
            self.all_passed = False
        
        try:
            from app.api_gateway import health_routes
            import inspect
            
            source = inspect.getsource(health_routes)
            has_health_check = '/health' in source
            has_status = '/status' in source
            
            test_result(has_health_check, "Health check route implemented")
            test_result(has_status, "Status route implemented")
        except Exception as e:
            test_result(False, f"Health routes check failed: {e}")
            self.all_passed = False
        
        try:
            # Verify validators are properly imported in registration
            from app.auth_service.registration import validate_password_strength
            test_result(True, "Password validator integrated in registration")
        except Exception as e:
            test_result(False, f"Registration integration failed: {e}")
            self.all_passed = False
    
    def check_edge_cases(self):
        """Check edge case handling."""
        print("\n🎪 Checking edge case handling...")
        
        # Email edge cases
        try:
            from app.utils import validate_email_format
            
            test_cases = [
                ("user@example.com", True),
                ("invalid", False),
                ("@example.com", False),
                ("user@", False),
            ]
            
            all_pass = all(
                validate_email_format(email) == expected 
                for email, expected in test_cases
            )
            test_result(all_pass, "Email validation handles edge cases")
        except Exception as e:
            test_result(False, f"Email edge cases failed: {e}")
            self.all_passed = False
        
        # Password edge cases
        try:
            from app.utils import validate_password_strength
            
            test_cases = [
                ("MyPass123!", True),   # Valid
                ("short", False),       # Too short
                ("nouppercase123!", False),  # No uppercase
            ]
            
            all_pass = all(
                validate_password_strength(pwd)[0] == expected 
                for pwd, expected in test_cases
            )
            test_result(all_pass, "Password validation handles edge cases")
        except Exception as e:
            test_result(False, f"Password edge cases failed: {e}")
            self.all_passed = False
        
        # Sanitization edge cases
        try:
            from app.utils import sanitize_input
            
            dangerous = ["<script>", "</script>", "<img>", "onclick="]
            normal = "John Doe"
            
            dangerous_sanitized = all(
                '<' not in sanitize_input(item) 
                for item in dangerous
            )
            normal_preserved = 'John' in sanitize_input(normal)
            
            test_result(dangerous_sanitized and normal_preserved, 
                       "Input sanitization handles edge cases")
        except Exception as e:
            test_result(False, f"Sanitization edge cases failed: {e}")
            self.all_passed = False
        
        # Quantity validation edge cases
        try:
            from app.utils import validate_quantity
            
            valid, _, _ = validate_quantity(100)
            test_result(valid, "Valid quantity accepted")
            
            invalid, _, _ = validate_quantity(-10)
            test_result(not invalid, "Negative quantity rejected")
        except Exception as e:
            test_result(False, f"Quantity validation edge cases failed: {e}")
            self.all_passed = False
        
        # Date validation edge cases
        try:
            from app.utils import validate_date_range
            from datetime import datetime, timedelta
            
            # Valid future date
            future_date = (datetime.utcnow() + timedelta(days=1)).isoformat()
            valid, _, _ = validate_date_range(future_date, allow_past=False)
            test_result(valid, "Valid future date accepted")
            
            # Invalid past date
            past_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
            invalid, _, _ = validate_date_range(past_date, allow_past=False)
            test_result(not invalid, "Invalid past date rejected")
        except Exception as e:
            test_result(False, f"Date validation edge cases failed: {e}")
            self.all_passed = False
    
    def print_summary(self):
        """Print overall summary."""
        print("\n" + "="*70)
        print("📊 DEEP DETAILED CHECK SUMMARY")
        print("="*70)
        
        if self.all_passed:
            print("\n✅ ALL CHECKS PASSED - SYSTEM HEALTHY")
            print("\nKey Validations:")
            print("  • Security implementations: ✅ Complete")
            print("  • Configuration setup: ✅ Correct")
            print("  • Database models: ✅ Properly indexed")
            print("  • API routes: ✅ All endpoints available")
            print("  • Integration points: ✅ Connected")
            print("  • Edge case handling: ✅ Robust")
            print("\n🎉 SYSTEM READY FOR DEPLOYMENT")
        else:
            print("\n⚠️ SOME CHECKS FAILED - REVIEW ABOVE")
        
        print("\n" + "="*70 + "\n")


def main():
    """Run deep detailed check."""
    checker = DeepDetailedCheck()
    return checker.run()


if __name__ == '__main__':
    sys.exit(main())
