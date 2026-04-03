#!/usr/bin/env python3
"""
Quick verification script to check JWT + Database configuration
Run this to verify everything is properly configured
"""
import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\n🔍 Checking .env file...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("   ✗ .env file not found")
        return False
    
    required_keys = [
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'MYSQL_HOST',
        'MYSQL_USER',
        'MYSQL_PASSWORD',
        'MYSQL_DATABASE'
    ]
    
    with open(env_path) as f:
        env_content = f.read()
    
    missing = []
    for key in required_keys:
        if key not in env_content:
            missing.append(key)
    
    if missing:
        print(f"   ✗ Missing keys: {', '.join(missing)}")
        return False
    
    print("   ✓ .env file found with all required keys")
    return True

def check_dependencies():
    """Check if all required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'pymysql',
        'werkzeug'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   ✗ Missing packages: {', '.join(missing)}")
        print(f"   💡 Install with: pip install -r requirements.txt")
        return False
    
    print("   ✓ All required packages installed")
    return True

def check_config_files():
    """Check if config files exist."""
    print("\n📁 Checking configuration files...")
    
    files_to_check = [
        'backend/config.py',
        'backend/app/__init__.py',
        'backend/app/api_gateway/auth_routes.py',
        'backend/app/auth_service/__init__.py'
    ]
    
    missing = []
    for file_path in files_to_check:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"   ✗ Missing files: {', '.join(missing)}")
        return False
    
    print("   ✓ All configuration files present")
    return True

def check_jwk_in_config():
    """Verify JWT configuration in config.py."""
    print("\n🔐 Checking JWT configuration in config.py...")
    
    with open('backend/config.py', 'r') as f:
        config = f.read()
    
    jwt_checks = [
        ('JWT_SECRET_KEY', 'JWT_SECRET_KEY in config'),
        ('JWT_ACCESS_TOKEN_EXPIRES', 'JWT_ACCESS_TOKEN_EXPIRES in config')
    ]
    
    missing = []
    for check_str, description in jwt_checks:
        if check_str not in config:
            missing.append(description)
    
    if missing:
        print(f"   ✗ Missing: {', '.join(missing)}")
        return False
    
    print("   ✓ JWT configuration properly set up")
    return True

def check_database_config():
    """Verify database configuration in config.py."""
    print("\n🗄️  Checking database configuration...")
    
    with open('backend/config.py', 'r') as f:
        config = f.read()
    
    db_checks = [
        'SQLALCHEMY_DATABASE_URI',
        'SQLALCHEMY_TRACK_MODIFICATIONS',
        'DB_HOST',
        'DB_USER',
        'DB_PASSWORD',
        'DB_NAME'
    ]
    
    missing = []
    for check in db_checks:
        if check not in config:
            missing.append(check)
    
    if missing:
        print(f"   ✗ Missing: {', '.join(missing)}")
        return False
    
    print("   ✓ Database configuration properly set up")
    return True

def check_app_initialization():
    """Verify app/__init__.py has proper initialization."""
    print("\n⚙️  Checking Flask app initialization...")
    
    with open('backend/app/__init__.py', 'r') as f:
        app_init = f.read()
    
    required_items = [
        ('from flask_jwt_extended import JWTManager', 'JWTManager import'),
        ('jwt = JWTManager(app)', 'JWT initialization'),
        ('db = SQLAlchemy(app)', 'Database initialization'),
        ('from app import api_gateway', 'Routes import')
    ]
    
    missing = []
    for check_str, description in required_items:
        if check_str not in app_init:
            missing.append(description)
    
    if missing:
        print(f"   ✗ Missing: {', '.join(missing)}")
        return False
    
    print("   ✓ Flask app properly initialized")
    return True

def check_auth_routes():
    """Verify JWT is used in auth routes."""
    print("\n🔐 Checking authentication routes...")
    
    with open('backend/app/api_gateway/auth_routes.py', 'r') as f:
        routes = f.read()
    
    required_items = [
        ('from flask_jwt_extended import create_access_token', 'JWT import'),
        ('create_access_token(', 'Token generation'),
        ('/api/auth/login', 'Login endpoint')
    ]
    
    missing = []
    for check_str, description in required_items:
        if check_str not in routes:
            missing.append(description)
    
    if missing:
        print(f"   ✗ Missing: {', '.join(missing)}")
        return False
    
    print("   ✓ Authentication routes properly configured")
    return True

def main():
    """Run all checks."""
    print("=" * 60)
    print("JWT + DATABASE CONFIGURATION VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Environment Variables", check_env_file),
        ("Dependencies", check_dependencies),
        ("Configuration Files", check_config_files),
        ("JWT Config", check_jwk_in_config),
        ("Database Config", check_database_config),
        ("App Initialization", check_app_initialization),
        ("Auth Routes", check_auth_routes)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🚀 Your JWT + Database configuration is ready!")
        print("\nNext steps:")
        print("  1. Run: python test_jwt_db_integration.py")
        print("  2. Start backend: python run.py")
        print("  3. Test login: POST http://localhost:5000/api/auth/login")
        return 0
    else:
        print(f"⚠️  {total - passed} check(s) failed ({passed}/{total})")
        print("\nPlease fix the issues above before deploying.")
        return 1

if __name__ == '__main__':
    # Change to backend directory if running from project root
    if Path('backend').exists() and not Path('backend/config.py').exists():
        os.chdir('backend')
    
    sys.exit(main())
