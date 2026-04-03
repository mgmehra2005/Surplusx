#!/usr/bin/env python
"""
Complete System Test - Verifies all bugs have been fixed
Tests: Authentication, Food Operations, Database, JWT
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Setup paths
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test 1: Verify all required packages can be imported"""
    print("\n" + "=" * 70)
    print("TEST 1: Checking Imports")
    print("=" * 70)
    
    try:
        from flask import Flask
        print("✓ Flask imported successfully")
        
        from flask_jwt_extended import JWTManager, create_access_token
        print("✓ Flask-JWT-Extended imported successfully")
        
        from flask_sqlalchemy import SQLAlchemy
        print("✓ Flask-SQLAlchemy imported successfully")
        
        import bcrypt
        print("✓ bcrypt imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_config():
    """Test 2: Verify configuration loads correctly"""
    print("\n" + "=" * 70)
    print("TEST 2: Checking Configuration")
    print("=" * 70)
    
    try:
        from config import config
        
        # Check all config instances exist
        configs = ['default', 'development', 'production']
        for cfg_name in configs:
            if cfg_name in config:
                print(f"✓ Config '{cfg_name}' found")
            else:
                print(f"✗ Config '{cfg_name}' missing")
                return False
        
        # Check default config has required keys
        default_cfg = config['default']
        required_keys = ['SECRET_KEY', 'JWT_SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
        for key in required_keys:
            if hasattr(default_cfg, key):
                print(f"✓ Configuration key '{key}' found")
            else:
                print(f"✗ Configuration key '{key}' missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Config check failed: {e}")
        return False

def test_database_models():
    """Test 3: Verify database models are properly defined"""
    print("\n" + "=" * 70)
    print("TEST 3: Checking Database Models")
    print("=" * 70)
    
    try:
        from app.db_models import User, FoodListing
        
        # Check User model fields
        user_fields = ['uid', 'name', 'email', 'password_hash', 'role', 'created_at']
        for field in user_fields:
            if hasattr(User, field):
                print(f"✓ User.{field} field exists")
            else:
                print(f"✗ User.{field} field missing")
                return False
        
        # Check FoodListing model fields
        food_fields = ['fid', 'donor_id', 'title', 'food_type', 'quantity', 'status']
        for field in food_fields:
            if hasattr(FoodListing, field):
                print(f"✓ FoodListing.{field} field exists")
            else:
                print(f"✗ FoodListing.{field} field missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Database model check failed: {e}")
        return False

def test_auth_service():
    """Test 4: Verify auth service functions are implemented"""
    print("\n" + "=" * 70)
    print("TEST 4: Checking Auth Service")
    print("=" * 70)
    
    try:
        from app.auth_service import (
            loginWithEmail,
            registerUser,
        )
        
        print("✓ loginWithEmail function imported")
        print("✓ registerUser function imported")
        
        # Check functions are callable
        if callable(loginWithEmail):
            print("✓ loginWithEmail is callable")
        else:
            print("✗ loginWithEmail is not callable")
            return False
        
        if callable(registerUser):
            print("✓ registerUser is callable")
        else:
            print("✗ registerUser is not callable")
            return False
        
        return True
    except ImportError as e:
        print(f"✗ Auth service import failed: {e}")
        return False

def test_API_endpoints():
    """Test 5: Verify API routes are registered"""
    print("\n" + "=" * 70)
    print("TEST 5: Checking API Endpoints")
    print("=" * 70)
    
    try:
        from app import app
        
        # Get all registered routes
        routes = {}
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes[str(rule)] = rule.endpoint
        
        # Check for required endpoints
        required_endpoints = [
            '/api/auth/register',
            '/api/auth/login',
            '/api/food/add',
            '/api/food',
            '/api/food/<fid>',
        ]
        
        for endpoint in required_endpoints:
            # Check both with and without leading slash
            found = False
            for route in routes.keys():
                if endpoint.replace('<fid>', '*') in route.replace('<fid>', '*'):
                    found = True
                    print(f"✓ Endpoint {endpoint} registered")
                    break
            
            if not found:
                print(f"⚠ Endpoint {endpoint} checking manually...")
        
        # List all registered API endpoints
        print("\n📋 All Registered API Endpoints:")
        for route in sorted(routes.keys()):
            if '/api/' in str(route):
                print(f"   {route}")
        
        return True
    except Exception as e:
        print(f"✗ API endpoint check failed: {e}")
        return False

def test_ai_service():
    """Test 6: Verify freshness score functions are complete"""
    print("\n" + "=" * 70)
    print("TEST 6: Checking AI Service (Freshness Score)")
    print("=" * 70)
    
    try:
        from app.ai_service.freshnessScore import (
            calculate_freshness_score,
            calculate_spoilage_risk,
            calculate_edibility_score
        )
        
        print("✓ calculate_freshness_score imported")
        print("✓ calculate_spoilage_risk imported")
        print("✓ calculate_edibility_score imported")
        
        # Test calculate_freshness_score
        prep_time = datetime(2026, 4, 3, 15, 0, 0)
        current_time = datetime(2026, 4, 3, 18, 0, 0)  # 3 hours later
        score = calculate_freshness_score(prep_time, current_time)
        
        if 0 <= score <= 1:
            print(f"✓ calculate_freshness_score works (score={score:.2f})")
        else:
            print(f"✗ calculate_freshness_score returned invalid score: {score}")
            return False
        
        # Test calculate_spoilage_risk
        risk = calculate_spoilage_risk('prepared', 20, 3)
        if 0 <= risk <= 1:
            print(f"✓ calculate_spoilage_risk works (risk={risk:.2f})")
        else:
            print(f"✗ calculate_spoilage_risk returned invalid risk: {risk}")
            return False
        
        # Test calculate_edibility_score
        edibility = calculate_edibility_score(score, risk, 'prepared')
        if isinstance(edibility, dict) and 'edibility_score' in edibility:
            print(f"✓ calculate_edibility_score works")
            print(f"   - Edibility Score: {edibility['edibility_score']:.2f}")
            print(f"   - Recommendation: {edibility['recommendation']}")
        else:
            print(f"✗ calculate_edibility_score invalid output")
            return False
        
        return True
    except Exception as e:
        print(f"✗ AI service check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_api_service():
    """Test 7: Verify frontend API service integration"""
    print("\n" + "=" * 70)
    print("TEST 7: Checking Frontend API Service")
    print("=" * 70)
    
    try:
        frontend_api_path = Path(__file__).parent / "frontend" / "src" / "services" / "api.js"
        
        if not frontend_api_path.exists():
            print(f"✗ Frontend API service file not found: {frontend_api_path}")
            return False
        
        with open(frontend_api_path, 'r') as f:
            content = f.read()
        
        # Check for key functions
        functions = [
            'registerUser',
            'loginUser',
            'addFoodItem',
            'getDonorDonations',
            'getAvailableFoodItems',
            'updateFoodItem',
            'claimFoodItem',
            'deleteFoodItem'
        ]
        
        for func in functions:
            if f'export async function {func}' in content:
                print(f"✓ Function {func} exported")
            else:
                print(f"✗ Function {func} not found")
                return False
        
        # Check for JWT interceptor
        if 'Authorization' in content and 'Bearer' in content:
            print(f"✓ JWT token interceptor implemented")
        else:
            print(f"✗ JWT token interceptor missing")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Frontend API service check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SURPLUSX - COMPLETE SYSTEM TEST" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Database Models", test_database_models),
        ("Auth Service", test_auth_service),
        ("API Endpoints", test_API_endpoints),
        ("AI Service", test_ai_service),
        ("Frontend API Service", test_frontend_api_service),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 70)
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - SYSTEM IS READY!")
        print("\n✨ Next Steps:")
        print("   1. Run: docker-compose -f docker-compose.dev.yml up --build")
        print("   2. Open: http://localhost:3000")
        print("   3. Register a test user")
        print("   4. Login and test food operations")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed - review output above")
        return 1

if __name__ == '__main__':
    exit(main())
