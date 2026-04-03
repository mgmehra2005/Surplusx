#!/usr/bin/env python3
"""
Advanced Scenario Testing - Detailed Behavioral Verification
Tests specific user flows and API behaviors
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path.parent))

def print_header(text):
    print(f"\n{'='*70}")
    print(f"🔬 {text}")
    print('='*70)

def test_case(name, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    msg = f"{status}: {name}"
    if details:
        msg += f" - {details}"
    print(f"   {msg}")
    return passed

class AdvancedScenarioTesting:
    """Test real-world scenarios and user flows."""
    
    def __init__(self):
        self.results = []
        self.total = 0
        self.passed = 0
    
    def run(self):
        """Run all scenario tests."""
        print("\n" + "🧪"*35)
        print("ADVANCED SCENARIO & BEHAVIORAL TESTING")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("🧪"*35)
        
        self.test_email_workflows()
        self.test_password_workflows()
        self.test_data_validation()
        self.test_input_security()
        self.test_database_operations()
        self.test_api_contract()
        self.test_error_handling()
        
        self.print_final_summary()
        return 0 if self.passed == self.total else 1
    
    def test_email_workflows(self):
        """Test email handling workflows."""
        print_header("EMAIL WORKFLOW TESTING")
        
        from app.utils import normalize_email, validate_email_format
        
        # Test 1: Case insensitivity across registrations
        self.total += 1
        try:
            emails = [
                "User@Example.Com",
                "user@example.com",
                "USER@EXAMPLE.COM"
            ]
            normalized = [normalize_email(e) for e in emails]
            all_same = all(n == "user@example.com" for n in normalized)
            if test_case("Multiple case variations normalize to same email", all_same):
                self.passed += 1
        except Exception as e:
            test_case("Multiple case variations normalize", False, str(e))
        
        # Test 2: Valid email patterns
        self.total += 1
        try:
            valid_emails = [
                "user@example.com",
                "user.name@example.co.uk",
                "user+tag@example.com",
                "123@example.com"
            ]
            all_valid = all(validate_email_format(e) for e in valid_emails)
            if test_case("Valid email patterns accepted", all_valid):
                self.passed += 1
        except Exception as e:
            test_case("Valid email patterns", False, str(e))
        
        # Test 3: Invalid email patterns
        self.total += 1
        try:
            invalid_emails = [
                "notanemail",
                "@example.com",
                "user@",
                "user @example.com",
                "user@.com"
            ]
            none_valid = not any(validate_email_format(e) for e in invalid_emails)
            if test_case("Invalid email patterns rejected", none_valid):
                self.passed += 1
        except Exception as e:
            test_case("Invalid email patterns", False, str(e))
    
    def test_password_workflows(self):
        """Test password validation workflows."""
        print_header("PASSWORD WORKFLOW TESTING")
        
        from app.utils import validate_password_strength
        
        # Test 1: Strong password acceptance
        self.total += 1
        try:
            strong_passwords = [
                "MyPassword123!",
                "Secure@Password1",
                "Str0ng#Pwd"
            ]
            all_strong = all(validate_password_strength(p)[0] for p in strong_passwords)
            if test_case("Strong passwords accepted", all_strong):
                self.passed += 1
        except Exception as e:
            test_case("Strong passwords", False, str(e))
        
        # Test 2: Weak password rejection
        self.total += 1
        try:
            weak_passwords = [
                "short",           # Too short
                "nouppercase123!",  # No upper
                "NOLOWERCASE123!",  # No lower
                "NoDigits!",        # No digits
                "NoSpecial123"      # No special
            ]
            none_pass = not any(validate_password_strength(p)[0] for p in weak_passwords)
            if test_case("Weak passwords rejected", none_pass):
                self.passed += 1
        except Exception as e:
            test_case("Weak passwords", False, str(e))
        
        # Test 3: Error messages descriptive
        self.total += 1
        try:
            is_valid, message = validate_password_strength("short")
            has_message = len(message) > 0 and "short" not in message.lower()
            if test_case("Password failures have descriptive messages", has_message, f"Message: {message}"):
                self.passed += 1
        except Exception as e:
            test_case("Descriptive password messages", False, str(e))
    
    def test_data_validation(self):
        """Test data validation workflows."""
        print_header("DATA VALIDATION TESTING")
        
        from app.utils import validate_quantity, validate_date_range, sanitize_input
        
        # Test 1: Quantity validation
        self.total += 1
        try:
            valid, qty, _ = validate_quantity(100.5)
            invalid, _, _ = validate_quantity(-50)
            zero_invalid, _, _ = validate_quantity(0)
            
            conditions = [valid and qty == 100.5, not invalid, not zero_invalid]
            if test_case("Quantity validation correct", all(conditions)):
                self.passed += 1
        except Exception as e:
            test_case("Quantity validation", False, str(e))
        
        # Test 2: Date validation boundaries
        self.total += 1
        try:
            now = datetime.utcnow()
            future = (now + timedelta(days=1)).isoformat()
            past = (now - timedelta(days=1)).isoformat()
            
            valid_future, _, _ = validate_date_range(future, allow_past=False)
            invalid_past, _, _ = validate_date_range(past, allow_past=False)
            
            if test_case("Date validation respects boundaries", valid_future and not invalid_past):
                self.passed += 1
        except Exception as e:
            test_case("Date validation", False, str(e))
        
        # Test 3: XSS prevention
        self.total += 1
        try:
            dangerous_inputs = [
                "<script>alert('xss')</script>",
                "<img src=x onerror=alert('xss')>",
                "javascript:alert('xss')",
            ]
            
            all_safe = all(
                '<' not in sanitize_input(inp) 
                for inp in dangerous_inputs
            )
            
            if test_case("Dangerous inputs neutralized", all_safe):
                self.passed += 1
        except Exception as e:
            test_case("XSS prevention", False, str(e))
    
    def test_input_security(self):
        """Test input security measures."""
        print_header("INPUT SECURITY TESTING")
        
        from app.utils import sanitize_input, validate_name
        
        # Test 1: Normal input preservation
        self.total += 1
        try:
            normal_inputs = [
                "John Doe",
                "Jane Smith-Johnson",
                "O'Brien"
            ]
            
            preserved = all(
                inp.replace('-', '').replace("'", '').split()[0] in sanitize_input(inp)
                for inp in normal_inputs
            )
            
            if test_case("Normal input preserved", preserved):
                self.passed += 1
        except Exception as e:
            test_case("Normal input preservation", False, str(e))
        
        # Test 2: Name validation
        self.total += 1
        try:
            valid_names = ["John Doe", "Mary-Jane", "O'Brien"]
            invalid_names = ["", "J", "<script>"]
            
            all_valid = all(validate_name(n) for n in valid_names)
            none_invalid = not any(validate_name(n) for n in invalid_names)
            
            if test_case("Name validation works", all_valid and none_invalid):
                self.passed += 1
        except Exception as e:
            test_case("Name validation", False, str(e))
    
    def test_database_operations(self):
        """Test database model operations."""
        print_header("DATABASE OPERATION TESTING")
        
        from app import db
        from app.db_models import User, FoodListing
        
        # Test 1: User model structure
        self.total += 1
        try:
            required_user_fields = ['uid', 'name', 'email', 'password_hash', 'role', 'phone']
            user_fields = [col.name for col in User.__table__.columns]
            
            has_all_fields = all(field in user_fields for field in required_user_fields)
            if test_case("User model has all required fields", has_all_fields):
                self.passed += 1
        except Exception as e:
            test_case("User model structure", False, str(e))
        
        # Test 2: FoodListing model structure
        self.total += 1
        try:
            required_food_fields = ['fid', 'donor_id', 'title', 'food_type', 'quantity', 'expiry_date', 'status']
            food_fields = [col.name for col in FoodListing.__table__.columns]
            
            has_all_fields = all(field in food_fields for field in required_food_fields)
            if test_case("FoodListing model has all required fields", has_all_fields):
                self.passed += 1
        except Exception as e:
            test_case("FoodListing model structure", False, str(e))
        
        # Test 3: Index coverage
        self.total += 1
        try:
            user_indexes = [idx.name for idx in User.__table__.indexes]
            food_indexes = [idx.name for idx in FoodListing.__table__.indexes]
            
            user_indexed = any('email' in str(idx).lower() for idx in user_indexes)
            food_indexed = any('status' in str(idx).lower() for idx in food_indexes)
            
            if test_case("Critical tables have indexes", user_indexed and food_indexed):
                self.passed += 1
        except Exception as e:
            test_case("Index coverage", False, str(e))
    
    def test_api_contract(self):
        """Test API contracts and response formats."""
        print_header("API CONTRACT TESTING")
        
        from app import app
        
        # Test 1: All critical routes exist
        self.total += 1
        try:
            routes = {
                'auth_register': '/auth/register',
                'auth_login': '/auth/login',
                'food_get': '/food',
                'health': '/health'
            }
            
            all_routes = [rule.rule for rule in app.url_map.iter_rules()]
            has_all = all(
                any(route_path in r for r in all_routes)
                for route_path in routes.values()
            )
            
            if test_case("All critical API routes available", has_all):
                self.passed += 1
        except Exception as e:
            test_case("API routes", False, str(e))
        
        # Test 2: Routes have proper methods
        self.total += 1
        try:
            from app import app
            routes_methods = {}
            
            for rule in app.url_map.iter_rules():
                routes_methods[rule.rule] = list(rule.methods)
            
            has_auth = any('/auth/register' in r for r in routes_methods)
            has_post = any('POST' in routes_methods.get(r, []) for r in routes_methods if '/auth/register' in r)
            
            if test_case("Routes have correct HTTP methods", has_auth and has_post):
                self.passed += 1
        except Exception as e:
            test_case("Route HTTP methods", False, str(e))
    
    def test_error_handling(self):
        """Test error handling and edge cases."""
        print_header("ERROR HANDLING TESTING")
        
        from app.utils import validate_password_strength, validate_email_format
        
        # Test 1: Graceful failure on invalid input types
        self.total += 1
        try:
            # Validators should handle None gracefully by returning False
            result_none, msg_none = validate_password_strength(None)
            result_empty, msg_empty = validate_password_strength("")
            
            passed = (result_none is False) and (result_empty is False)
            
            if test_case("Invalid input types handled gracefully", passed):
                self.passed += 1
        except Exception as e:
            test_case("Invalid input type handling", False, str(e))
        
        # Test 2: All validators return tuples
        self.total += 1
        try:
            from app.utils import validate_password_strength, validate_date_range, validate_quantity
            
            pwd_result = validate_password_strength("Test123!")
            date_result = validate_date_range(datetime.utcnow().isoformat())
            qty_result = validate_quantity(100)
            
            all_tuples = all([
                isinstance(pwd_result, tuple),
                isinstance(date_result, tuple),
                isinstance(qty_result, tuple)
            ])
            
            if test_case("All validators return consistent format", all_tuples):
                self.passed += 1
        except Exception as e:
            test_case("Validator return format", False, str(e))
        
        # Test 3: Error messages are informative
        self.total += 1
        try:
            _, msg = validate_password_strength("short")
            has_info = len(msg) > 10 and "password" in msg.lower()
            
            if test_case("Error messages are informative", has_info, f"Message: {msg[:50]}..."):
                self.passed += 1
        except Exception as e:
            test_case("Informative error messages", False, str(e))
    
    def print_final_summary(self):
        """Print final summary."""
        print(f"\n{'='*70}")
        print("📊 SCENARIO TESTING SUMMARY")
        print('='*70)
        
        print(f"\nTotal Tests: {self.total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.total - self.passed}")
        print(f"Pass Rate: {(self.passed/self.total*100):.1f}%")
        
        if self.passed == self.total:
            print("\n✅ ALL SCENARIO TESTS PASSED")
            print("   Real-world workflows verified")
            print("   Error handling confirmed")
            print("   Data validation working correctly")
            print("\n🎯 SYSTEM BEHAVIOR VALIDATED")
        else:
            print("\n⚠️ SOME TESTS FAILED")
            print("   Review failures above")
        
        print('='*70 + "\n")


def main():
    """Run advanced scenario testing."""
    tester = AdvancedScenarioTesting()
    return tester.run()


if __name__ == '__main__':
    sys.exit(main())
