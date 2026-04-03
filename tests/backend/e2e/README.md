# 🚀 End-to-End (E2E) Tests

Complete system verification tests that check the entire application from startup to shutdown.

---

## 📁 Files

```
SYSTEM_TEST.py                  Complete system verification (7 tests)
test_auth_bugs_fixed.py         Auth bug fixes validation
```

---

## 🎯 Key Features

- ✅ **Complete System Verification** - Tests all components
- ✅ **Production Readiness** - Full validation before deployment
- ✅ **All Layers** - Backend, database, API, frontend integration
- ✅ **Comprehensive** - 7 major test areas
- ✅ **Pre-deployment Checklist** - Run before go-live

---

## 📄 File Documentation

### `SYSTEM_TEST.py`

**Purpose:** Comprehensive 7-test system verification

**Tests Included:**

#### ✅ Test 1: Import Validation
Verifies all required packages are installed and importable
- Flask, Flask-JWT-Extended, Flask-SQLAlchemy, bcrypt, etc.

#### ✅ Test 2: Configuration Check
Validates configuration loads correctly for all environments
- Development, production, testing configs
- Environment variables
- Database settings

#### ✅ Test 3: Database Models
Verifies all database models are defined and working
- User model and relationships
- FoodListing model and fields
- NGO, DeliveryPartner, Delivery models
- SystemLog model

#### ✅ Test 4: Auth Service
Validates authentication service functionality
- Password hashing (hashPassword)
- Password verification (checkPasswordHash)
- Email verification
- Bug fixes implementation

#### ✅ Test 5: API Endpoints
Tests all API routes and endpoints
- `/api/auth/register` - User registration
- `/api/auth/login` - User login
- `/api/food/add` - Add food items
- Response formats and status codes

#### ✅ Test 6: AI Service
Validates freshness scoring and predictions
- Freshness calculation
- Spoilage risk assessment
- Edibility scoring
- AI functions

#### ✅ Test 7: Frontend Integration
Verifies frontend can communicate with backend
- API client setup (Axios)
- JWT token handling
- Request/response formats
- Error handling

**Run:**
```bash
python SYSTEM_TEST.py
```

**Expected Output:**
```
======================================================================
SYSTEM_TEST: Complete System Verification
======================================================================

TEST 1: Checking Imports
✓ Flask imported successfully
✓ Flask-JWT-Extended imported successfully
✓ Flask-SQLAlchemy imported successfully
✓ bcrypt imported successfully

[... more tests ...]

======================================================================
FINAL RESULT: ✅ All 7 tests passed! System is ready.
======================================================================
```

---

### `test_auth_bugs_fixed.py`

**Purpose:** Validate all authentication bugs have been fixed

**What it tests:**
- ✓ Registration endpoint works
- ✓ Login returns JWT token
- ✓ Password hashing is secure
- ✓ Email verification works
- ✓ Role-based access control
- ✓ Token validation on protected routes
- ✓ Previous bug fixes still working

**Bug Coverage:**
- ✓ Registration was disabled
- ✓ Login didn't return JWT
- ✓ Hardcoded data was used
- ✓ Insecure email-based roles
- ✓ Missing input validation
- ✓ Inconsistent role names

**Run:**
```bash
python test_auth_bugs_fixed.py
```

---

## 🚀 Run All E2E Tests

```bash
# Individual execution
python SYSTEM_TEST.py
python test_auth_bugs_fixed.py

# Using pytest
python -m pytest test_*.py SYSTEM_TEST.py -v

# With detailed output
python -m pytest -v -s

# Stop on first failure
python -m pytest -x
```

---

## 📊 Expected Output

```
SYSTEM_TEST.py
✓ TEST 1: Imports - PASS
✓ TEST 2: Configuration - PASS
✓ TEST 3: Database Models - PASS
✓ TEST 4: Auth Service - PASS
✓ TEST 5: API Endpoints - PASS
✓ TEST 6: AI Service - PASS
✓ TEST 7: Frontend Integration - PASS

Result: ✅ All 7 tests passed!

test_auth_bugs_fixed.py
✓ Registration endpoint - PASS
✓ Login with JWT - PASS
✓ Password hashing - PASS
✓ Role-based access - PASS
✓ Previous fixes - PASS

Result: ✅ All auth tests passed!

TOTAL: 12/12 tests passed ✅
```

---

## 🎓 When to Use E2E Tests

✅ **Use E2E tests for:**
- Pre-deployment verification
- After major changes
- Release validation
- System-wide health checks
- User workflow validation
- Complete feature testing

❌ **Don't use for:**
- Unit testing components (use unit tests)
- Quick iterations (use unit tests)
- Every code change (too slow)
- Performance testing (use performance tests)
- Load testing (use load tests)

---

## 🔄 Pre-Deployment Checklist

Run E2E tests before deploying:

```bash
# 1. Run system test
python SYSTEM_TEST.py

# Expected: ✅ All 7 tests passed!

# 2. Run auth bugs test
python test_auth_bugs_fixed.py

# Expected: ✅ All auth tests passed!

# 3. Check database is up
mysql -u root -p -e "USE surplusx; SELECT COUNT(*) FROM users;"

# 4. Check backend is running
curl http://localhost:5000/api/health

# 5. Check frontend builds
cd frontend && npm run build

# 6. All clear - ready to deploy!
echo "✅ System ready for deployment"
```

---

## 📈 Test Coverage

This E2E test suite validates:

| Component | Coverage | Status |
|-----------|----------|--------|
| **Imports** | All packages | ✅ |
| **Configuration** | All environments | ✅ |
| **Database** | All models | ✅ |
| **Auth** | Register, login, JWT | ✅ |
| **API** | All endpoints | ✅ |
| **AI** | Freshness scoring | ✅ |
| **Frontend** | Integration layer | ✅ |

---

## 🔧 Debugging E2E Tests

### See Detailed Output
```bash
python SYSTEM_TEST.py -v
```

### Test Specific Component
```bash
# Edit SYSTEM_TEST.py to comment out tests
# and run individual sections
```

### Check Database State
```bash
# During test, check what's in database
mysql -u root -p surplusx
> SELECT * FROM users;
> SELECT COUNT(*) FROM food_listings;
```

### Review Logs
```bash
# Check backend logs
tail -f backend.log

# Check database logs
tail -f mysql.log
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

### Database Connection Failed
```
Error connecting to MySQL server
```
**Solution:** Start database first
```bash
# Using Docker
docker-compose -f docker-compose.dev.yml up

# Or local MySQL
mysql.server start
```

### API Endpoint Failed
```
ConnectionError: Failed to connect to backend
```
**Solution:** Start backend server
```bash
cd backend
python run.py
```

### Configuration Missing
```
KeyError: 'DATABASE_URL'
```
**Solution:** Ensure .env file exists
```bash
# Copy .env.example to .env
cp .env.example .env
```

---

## 🎯 System Requirements

| Component | Required | Version |
|-----------|----------|---------|
| **Python** | ✅ | 3.9+ |
| **MySQL** | ✅ | 8.0 |
| **Flask** | ✅ | 3.1.3 |
| **Node.js** | ✅ (for frontend) | 16+ |
| **Docker** | ⚠️ (optional) | 20.10+ |

---

## 📋 Test Execution Plan

```
┌─ E2E Test Start
│
├─ Setup: Verify environment, database, config
│ 
├─ Test 1-2: Check imports and configuration
│
├─ Test 3: Validate database models
│
├─ Test 4: Test authentication service
│
├─ Test 5: Run API endpoint tests
│
├─ Test 6: Verify AI service
│
├─ Test 7: Check frontend integration
│
├─ Cleanup: Close connections, cleanup
│
└─ Result: Pass/Fail with summary
```

---

## 🔗 Related

- [Unit Tests](../unit/README.md)
- [Integration Tests](../integration/README.md)
- [Backend Tests](../README.md)
- [All Tests](../../README.md)
- [Setup Guide](../../../docs/getting-started/SETUP_GUIDE.md)

---

## 📞 Support

If E2E tests fail:

1. **Check output message** - Usually indicates which component failed
2. **Review setup guide** - Ensure everything is configured correctly
3. **Check database** - Verify MySQL is running and accessible
4. **Check backend** - Verify Flask server is running
5. **Review .env file** - Verify all required variables are set
6. **Check logs** - Look for error details in console output

---

**Location:** `tests/backend/e2e/`  
**Status:** ✅ Ready to use  
**Last Updated:** April 3, 2026  
**Expected Runtime:** ~5-10 seconds

✅ **Use these tests before every deployment!**
