# 🔬 Unit Tests

Fast, isolated tests of individual components with no external dependencies.

---

## 📁 Files

```
test_jwt_standalone.py          JWT token generation/validation in memory
test_auth_service_bugs.py       Auth service module functionality
```

---

## ⚡ Key Features

- ✅ **No Database Needed** - Use in-memory SQLite
- ✅ **Super Fast** - Run in milliseconds
- ✅ **Isolated** - No external dependencies
- ✅ **Good for Development** - Quick feedback loop
- ✅ **Easy to Debug** - Simple, focused tests

---

## 📄 File Documentation

### `test_jwt_standalone.py`

**Purpose:** Test JWT authentication in complete isolation

**What it tests:**
- ✓ User model definition
- ✓ Token generation (create_access_token)
- ✓ Password hashing (werkzeug)
- ✓ Token decoding/validation
- ✓ JWT secret configuration

**Run:**
```bash
python test_jwt_standalone.py
```

**Dependencies:**
- Flask
- Flask-SQLAlchemy (in-memory SQLite)
- Flask-JWT-Extended
- werkzeug

---

### `test_auth_service_bugs.py`

**Purpose:** Test auth service module functions

**What it tests:**
- ✓ Password hashing (hashPassword)
- ✓ Password verification (checkPasswordHash)
- ✓ Email verification (verifyEmail)
- ✓ Email-based password verification
- ✓ Bug fixes from previous iterations
- ✓ Edge cases and error handling

**Run:**
```bash
python test_auth_service_bugs.py
```

**Dependencies:**
- App from actual project
- Database models
- Auth service functions

---

## 🚀 Run All Unit Tests

```bash
# Individual execution
python test_jwt_standalone.py
python test_auth_service_bugs.py

# Using pytest
python -m pytest test_*.py -v

# With output
python -m pytest test_*.py -v -s
```

---

## 📊 Expected Output

```
✓ test_jwt_standalone.py
  ├─ Token generation: PASS
  ├─ Token validation: PASS
  └─ User model: PASS

✓ test_auth_service_bugs.py
  ├─ Password hashing: PASS
  ├─ Email verification: PASS
  └─ Edge cases: PASS

Total: 2/2 tests passed ✅
```

---

## 🎓 When to Use Unit Tests

✅ **Use unit tests for:**
- New feature implementation
- Bug fixes
- Refactoring code
- Testing utility functions
- Rapid iteration during development

❌ **Don't use for:**
- Database interactions (use integration tests)
- API calls (use integration tests)
- Multiple components (use integration tests)
- Full workflows (use E2E tests)

---

## 💡 Best Practices

### 1. Keep Tests Small
```python
# Good: One thing per test
def test_password_hashing():
    hashed = hashPassword("test123")
    assert checkPasswordHash("test123", hashed)

# Bad: Many things in one test
def test_everything():
    # ... 50 lines testing multiple things
```

### 2. Use Descriptive Names
```python
# Good
def test_hash_password_with_special_characters()

# Bad
def test_hash()
```

### 3. No External Dependencies
```python
# Good: In-memory SQLite
config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Bad: Real database
config['SQLALCHEMY_DATABASE_URI'] = 'mysql://...'
```

### 4. Fast Execution
```python
# Good: Completes in < 100ms
python test_jwt_standalone.py
# Time: 0.045s

# Bad: Takes seconds
# Should move to integration tests
```

---

## 🔧 Debugging Unit Tests

### Print Debug Output
```bash
# Run with -s to capture prints
python -m pytest test_jwt_standalone.py -v -s
```

### Verbose Mode
```bash
# See all assertions
python -m pytest test_auth_service_bugs.py -vv
```

### Stop on First Failure
```bash
# Exit immediately on failure
python -m pytest test_*.py -x
```

---

## ❌ Troubleshooting

### Import Errors
```
ImportError: No module named 'flask'
```
**Solution:** Install requirements
```bash
pip install -r ../../backend/requirements.txt
```

### Database Errors
```
sqlite: database is locked
```
**Solution:** These tests use in-memory SQLite, shouldn't happen
- Check if another test is running
- Try deleting `.pytest_cache/`

### Configuration Errors
```
KeyError: 'SECRET_KEY'
```
**Solution:** Tests set config internally, shouldn't happen
- Check test file setup
- Check FLASK_ENV variable

---

## 📈 Metrics

| Metric | Value |
|--------|-------|
| **Total Tests** | 2 |
| **Lines of Code** | ~300 |
| **Execution Time** | < 1 second |
| **Dependencies** | 4 (Flask, SQLAlchemy, JWT, bcrypt) |
| **Coverage** | Auth service functions |

---

## 🔗 Related

- [Backend Tests](../README.md)
- [Integration Tests](../integration/README.md)
- [E2E Tests](../e2e/README.md)
- [All Tests](../../README.md)
- [Setup Guide](../../../docs/getting-started/SETUP_GUIDE.md)

---

**Location:** `tests/backend/unit/`  
**Status:** ✅ Ready to use  
**Last Updated:** April 3, 2026
