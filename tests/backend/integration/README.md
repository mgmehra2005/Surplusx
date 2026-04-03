# 🔗 Integration Tests

Medium-speed tests that verify multiple components work together properly.

---

## 📁 Files

```
test_jwt_db_integration.py       JWT + Database working together
test_jwt.py                      JWT workflow and functionality
```

---

## 🎯 Key Features

- ✅ **Test Component Interaction** - Multiple parts working together
- ✅ **Use Real Database** - SQLite for testing (not in-memory)
- ✅ **Moderate Speed** - Slower than unit, faster than E2E
- ✅ **Realistic Scenarios** - Tests actual use cases
- ✅ **Good for QA** - Catches integration bugs

---

## 📄 File Documentation

### `test_jwt_db_integration.py`

**Purpose:** Test JWT authentication with actual database persistence

**What it tests:**
- ✓ User creation and persistence to database
- ✓ Token generation for authenticated users
- ✓ Token validation against database
- ✓ JWT claims extraction
- ✓ Protected route access with JWT
- ✓ Multi-user scenarios
- ✓ Token expiration handling

**Scenario:**
```
1. Create user in database
2. Generate JWT token
3. Validate token matches database user
4. Test protected endpoint access
5. Verify claims contain correct user info
```

**Run:**
```bash
python test_jwt_db_integration.py
```

**Dependencies:**
- Flask with testing config
- SQLAlchemy with test database
- Flask-JWT-Extended
- werkzeug for password hashing

---

### `test_jwt.py`

**Purpose:** Test JWT workflow and functionality

**What it tests:**
- ✓ JWT creation with correct claims
- ✓ Token parsing and validation
- ✓ User identity extraction from token
- ✓ Token-protected endpoints
- ✓ Authorization checks
- ✓ Edge cases and error scenarios

**Scenario:**
```
1. Create JWT token with user data
2. Decode and verify token structure
3. Extract user identity
4. Test endpoint protection
5. Test unauthorized access
```

**Run:**
```bash
python test_jwt.py
```

**Dependencies:**
- Flask JWT-Extended
- SQLAlchemy models
- Firebase/auth mechanisms

---

## 🚀 Run All Integration Tests

```bash
# Individual execution
python test_jwt_db_integration.py
python test_jwt.py

# Using pytest
python -m pytest test_*.py -v

# With detailed output
python -m pytest test_*.py -v -s

# With coverage
python -m pytest test_*.py --cov=../../app
```

---

## 📊 Expected Output

```
test_jwt_db_integration.py
✓ User creation and persistence: PASS
✓ Token generation: PASS
✓ Token validation: PASS
✓ Protected access: PASS
✓ Multi-user scenarios: PASS

test_jwt.py
✓ JWT token creation: PASS
✓ Token parsing: PASS
✓ User identity extraction: PASS
✓ Endpoint protection: PASS
✓ Error handling: PASS

Total: 2/2 tests passed ✅
```

---

## 🎓 When to Use Integration Tests

✅ **Use integration tests for:**
- Testing API endpoints
- Database persistence
- Component interaction
- JWT with user authentication
- Login/register workflows
- Data flow between services

❌ **Don't use for:**
- Single component testing (use unit tests)
- UI testing (use E2E tests)
- Load testing (use performance tests)
- External API testing (use mocks)

---

## 💡 Best Practices

### 1. Use Test Database
```python
# Good: Isolated test database
db_uri = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Good: In-memory for speed
db_uri = 'sqlite:///:memory:'

# Bad: Production database
db_uri = 'mysql://prod:password@localhost'
```

### 2. Setup and Teardown
```python
# Good: Clean state for each test
def setup():
    db.create_all()

def teardown():
    db.session.remove()
    db.drop_all()

# Bad: Tests interfere with each other
# (no setup/teardown)
```

### 3. Test Real Scenarios
```python
# Good: Real user workflow
1. Register user
2. Login (get token)
3. Access protected endpoint

# Bad: Just testing isolated functions
```

### 4. Verify Side Effects
```python
# Good: Check database after operation
user = create_user_via_api(...)
assert User.query.filter_by(email=email).first() is not None

# Bad: Just check return value
assert response.status_code == 201
```

---

## 🔄 Test Flow

```
┌─ Start Test
│
├─ Setup: Create test database, tables
│
├─ Execute: Create user → Generate token → Use token
│
├─ Assert: Verify results, database state, claims
│
└─ Teardown: Clean database, close connections
```

---

## 🔧 Debugging Integration Tests

### Print Request/Response
```bash
python -m pytest test_jwt_db_integration.py -v -s
```

### Debug Database State
```python
# Add to test
print(User.query.all())
print(db.session.query(User).count())
```

### Inspect Token
```python
# Decode token to see claims
from flask_jwt_extended import decode_token
print(decode_token(token))
```

### Test Individual Steps
```bash
# Run specific test
python -m pytest test_jwt_db_integration.py::test_user_creation -v
```

---

## ❌ Troubleshooting

### Database Locked
```
sqlite: database is locked
```
**Solution:** Ensure teardown closes connections
```python
def teardown():
    db.session.close()
    db.drop_all()
```

### Token Validation Fails
```
Exception: Missing Authorization Header
```
**Solution:** Add JWT to request headers
```python
headers = {'Authorization': f'Bearer {token}'}
response = client.get('/api/food', headers=headers)
```

### User Not Found
```
AssertionError: User creation failed
```
**Solution:** Check setup creates tables
```python
db.create_all()  # Before first test
assert User.query.first() is not None
```

---

## 📈 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| **Execution Time** | < 5s | ~2s |
| **Tests** | 2+ | 2 |
| **Database Ops** | < 10 per test | ~5 |
| **Memory** | < 100MB | ~50MB |

---

## 🔗 Related

- [Unit Tests](../unit/README.md)
- [E2E Tests](../e2e/README.md)
- [Backend Tests](../README.md)
- [All Tests](../../README.md)
- [Setup Guide](../../../docs/getting-started/SETUP_GUIDE.md)

---

**Location:** `tests/backend/integration/`  
**Status:** ✅ Ready to use  
**Last Updated:** April 3, 2026
