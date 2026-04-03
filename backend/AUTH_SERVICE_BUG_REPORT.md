# Auth Service Bug Report

## Summary
The test suite identified **3 bugs** in the `auth_service` module of the SurplusX application.

---

## Bug #1: Missing `registerUser` Function (CRITICAL)

**Severity:** CRITICAL  
**Status:** Not Implemented  
**Location:** `app/auth_service/__init__.py`

### Description
The `registerUser` function is **not exported** or **not implemented** in the `__init__.py` file. This function is essential for user registration but is commented out in `registration.py`.

### Current State
- File: [backend/app/auth_service/registration.py](backend/app/auth_service/registration.py)
  - Line 4 shows: `# def registerUser(username: str, email: str, password: str) -> bool:`
  - The function is **commented out** and not implemented

- File: [backend/app/auth_service/__init__.py](backend/app/auth_service/__init__.py)
  - Only exports: `loginWithEmail`
  - Missing: `registerUser` export

### Impact
- Users cannot register new accounts via the API
- The `/api/auth/register` endpoint (if it exists) will fail
- Registration flow is broken

### Fix Required
1. Implement the `registerUser` function in `registration.py`
2. Export it from `__init__.py` for use in API routes
3. Add proper validation and error handling

### Test Results
```
✗ FAIL: registerUser function exists
       BUG FOUND: registerUser is not exported or implemented in __init__.py
```

---

## Bug #2: Email Case Sensitivity Issue (HIGH)

**Severity:** HIGH  
**Status:** Design Issue  
**Location:** `app/auth_service/verification.py` and `app/auth_service/__init__.py`

### Description
The email verification functions are **case-sensitive** during login. Users cannot login with email addresses that use different case variations (e.g., "Test@Example.com" vs "test@example.com").

### Current State
- `verifyEmail()` uses: `User.query.filter_by(email=email).first()`
- `verifyPasswordByEmail()` uses: `User.query.filter_by(email=email).first()`
- SQLite/MySQL email comparison is **case-sensitive by default**

### Example Failure
```
User registered with: CaseSensitive@Example.COM
Login attempt with:   casesensitive@example.com
Result: ✗ FAILS (should succeed)
```

### Impact
- Users get "Invalid email or password" errors when using different email case
- Poor user experience (users don't expect email case to matter)
- Potential security issue if user is unaware of correct case

### Test Results
```
✓ PASS: Login with exact case
       Should succeed with exact case
✗ FAIL: Login with lowercase email
       Expected success, got failure - DB column is case-sensitive
```

### Fix Required
Convert emails to lowercase before querying:
```python
def verifyEmail(email: str) -> bool:
    if not email:
        return False
    user = User.query.filter_by(email=email.lower()).first()
    return user is not None

def verifyPasswordByEmail(email: str, password: str) -> bool:
    if not email or not password:
        return False
    
    user = User.query.filter_by(email=email.lower()).first()
    if not user:
        return False
    
    return checkPasswordHash(password, user.password_hash)
```

---

## Bug #3: No Graceful Handling of NULL password_hash (MEDIUM)

**Severity:** MEDIUM  
**Status:** Design Issue  
**Location:** `app/auth_service/verification.py`

### Description
The code doesn't gracefully handle the scenario where a user record exists but has a NULL `password_hash`. The database constraint prevents this, but the code should handle it defensively.

### Current State
- Database has: `password_hash = db.Column(db.String(255), nullable=False)`
- The constraint prevents NULL values at DB level
- Code tries to check empty string: `if _password_hash_ == ""`
- But doesn't handle None/NULL values from potential DB corruption

### Potential Issues
```python
def __getPasswordHashByEmail__(email: str) -> str:
    user = User.query.filter_by(email=email).first()
    return user.password_hash if user else ""  # Returns "" but could be None from DB
```

### Test Results
```
✗ FAIL: NULL password hash test
       Setup exception: (sqlite3.IntegrityError) NOT NULL constraint failed: users.password_hash
```

### Impact
- LOW in production (DB constraint prevents this)
- MEDIUM for defensive programming and future database migrations

### Fix Required
Add explicit None checks:
```python
def __getPasswordHashByEmail__(email: str) -> str:
    """Fetch password hash by email."""
    user = User.query.filter_by(email=email).first()
    if not user or not user.password_hash:
        return ""
    return user.password_hash
```

---

## Test Execution Summary

**Total Tests:** 26  
**Passed:** 23 ✓  
**Failed:** 3 ✗  

### Tests Passed
- ✓ Password hashing (4/4)
- ✓ Email verification (4/4)
- ✓ Password verification by email (7/7)
- ✓ Login with email (6/6)
- ✓ Email case sensitivity - exact case (1/1)

### Tests Failed
- ✗ Registration function availability (1/1)
- ✗ NULL password hash handling (1/1)
- ✗ Email case sensitivity - lowercase (1/1)

---

## Recommendations

### Priority 1 (Do First)
1. **Implement `registerUser` function** - This is blocking user registration
2. **Fix email case sensitivity** - Critical for user experience

### Priority 2 (Do Next)
3. **Add defensive NULL checks** - Prevent potential edge cases

### Priority 3 (Consider)
- Add rate limiting to login attempts
- Add logging for auth failures
- Add password complexity validation for registration
- Add email verification/validation

---

## Files to Modify

1. **backend/app/auth_service/registration.py**
   - Uncomment and properly implement `registerUser()`
   - Add validation for input parameters
   - Add error handling

2. **backend/app/auth_service/verification.py**
   - Add `.lower()` to email comparisons in `verifyEmail()` and `verifyPasswordByEmail()`
   - Improve NULL handling in `__getPasswordHashByEmail__()`

3. **backend/app/auth_service/__init__.py**
   - Export `registerUser` function
   - Import it from registration module

4. **backend/app/api_gateway/auth_routes.py**
   - Add `/api/auth/register` endpoint if not already present
   - Use the `registerUser` function for registration

---

## Test File Location
- **Test File:** `backend/test_auth_service_bugs.py`
- **Run Command:** `python test_auth_service_bugs.py`
