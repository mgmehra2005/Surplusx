# 🧪 Test Suite Documentation

Welcome to the SurplusX test suite! This folder contains all automated tests organized by type and scope.

---

## 📁 Test Structure

```
tests/
└── backend/
    ├── unit/              # Isolated component tests
    ├── integration/       # Multi-component tests
    └── e2e/              # Full system tests
```

---

## 🎯 Quick Start

### Run All Tests
```bash
# From project root
python -m pytest tests/ -v

# Or individual test types
python tests/backend/unit/test_jwt_standalone.py
python tests/backend/integration/test_jwt_db_integration.py
python tests/backend/e2e/SYSTEM_TEST.py
```

### Run Specific Test File
```bash
# Unit tests
python tests/backend/unit/test_jwt_standalone.py
python tests/backend/unit/test_auth_service_bugs.py

# Integration tests
python tests/backend/integration/test_jwt_db_integration.py
python tests/backend/integration/test_jwt.py

# End-to-end tests  
python tests/backend/e2e/SYSTEM_TEST.py
python tests/backend/e2e/test_auth_bugs_fixed.py
```

---

## 📚 Test Categories

### 🔬 Unit Tests (`tests/backend/unit/`)
**Purpose:** Test individual components in isolation

**Files:**
- `test_jwt_standalone.py` - JWT authentication without database dependencies
- `test_auth_service_bugs.py` - Auth service module functionality

**When to use:**
- Testing password hashing functions
- Testing token generation in isolation
- Verifying utility functions
- Fast feedback during development

**Run:**
```bash
python tests/backend/unit/test_jwt_standalone.py
python tests/backend/unit/test_auth_service_bugs.py
```

---

### 🔗 Integration Tests (`tests/backend/integration/`)
**Purpose:** Test multiple components working together

**Files:**
- `test_jwt_db_integration.py` - JWT + Database integration
- `test_jwt.py` - JWT and related components

**When to use:**
- Testing JWT with database
- Verifying API endpoints
- Testing data flow between components
- Validating complex workflows

**Run:**
```bash
python tests/backend/integration/test_jwt_db_integration.py
python tests/backend/integration/test_jwt.py
```

---

### 🚀 End-to-End Tests (`tests/backend/e2e/`)
**Purpose:** Test complete user workflows and system behavior

**Files:**
- `SYSTEM_TEST.py` - Full system verification (7 comprehensive tests)
  - ✓ Import validation
  - ✓ Configuration checks
  - ✓ Database model verification
  - ✓ Auth service validation
  - ✓ API endpoint functionality
  - ✓ AI service verification
  - ✓ Frontend integration
  
- `test_auth_bugs_fixed.py` - Auth bug fixes verification

**When to use:**
- Pre-deployment verification
- After major changes
- Release validation
- System-wide health checks

**Run:**
```bash
python tests/backend/e2e/SYSTEM_TEST.py
python tests/backend/e2e/test_auth_bugs_fixed.py
```

---

## 🔄 Test Hierarchy

```
┌─ Unit Tests (Fast, Isolated)
│  ├─ Password hashing
│  ├─ Token generation
│  └─ Service functions
│
├─ Integration Tests (Medium, Connected)
│  ├─ JWT + DB workflows
│  ├─ API endpoints
│  └─ Data persistence
│
└─ E2E Tests (Slow, Complete)
   ├─ Full system flow
   ├─ All components together
   └─ Production readiness
```

---

## 📊 Test Summary

| Type | Count | Purpose | Speed |
|------|-------|---------|-------|
| **Unit** | 2 | Component isolation | ⚡ Very Fast |
| **Integration** | 2 | Component interaction | ⚡ Fast |
| **E2E** | 2 | Full system | 🐢 Slower |
| **Total** | 6 | Complete coverage | - |

---

## 🚀 Running Tests from Docker

### Development Environment
```bash
# Terminal 1: Start services
docker-compose -f docker-compose.dev.yml up --build

# Terminal 2: Run tests in backend container
docker-compose -f docker-compose.dev.yml exec backend python tests/backend/e2e/SYSTEM_TEST.py
```

### Local Development
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run specific test suite
python tests/backend/unit/test_jwt_standalone.py
python tests/backend/integration/test_jwt_db_integration.py
python tests/backend/e2e/SYSTEM_TEST.py
```

---

## ✅ Expected Results

### ✓ Passing Tests
- All unit tests should pass (isolated, no dependencies)
- Integration tests verify JWT + DB working together
- E2E SYSTEM_TEST.py returns: "✅ All 7 tests passed!"

### ❌ Troubleshooting Failures
1. **Import Errors** - Check `backend/requirements.txt` installed
2. **Database Errors** - Ensure MySQL/SQLite accessible
3. **JWT Errors** - Verify `.env` has `SECRET_KEY` set
4. **API Errors** - Ensure backend is running for integration tests

---

## 📝 Test File Details

### `test_jwt_standalone.py`
- Tests JWT in memory with SQLite
- No external dependencies
- Validates: token generation, decoding, user model

### `test_auth_service_bugs.py`  
- Tests authentication service functions
- Validates: password hashing, email verification
- Tests: edge cases, bug fixes

### `test_jwt_db_integration.py`
- Tests JWT with real database
- Validates: login flow, token persistence
- Tests: concurrent users, token expiration

### `test_jwt.py`
- General JWT testing
- Validates: token generation, validation
- Tests: authorization flows

### `SYSTEM_TEST.py`
- Complete system validation
- 7 comprehensive tests covering all components
- Returns pass/fail summary

### `test_auth_bugs_fixed.py`
- Verifies auth bug fixes
- Tests: registration, login, token handling
- Validates: edge cases fixed

---

## 🎓 Understanding Test Organization

### Why This Structure?

```
tests/backend/
├── unit/          ← Test one component at a time
├── integration/   ← Test components together  
└── e2e/          ← Test entire system
```

**Benefits:**
- ✅ Clear organization
- ✅ Easy to locate tests
- ✅ Scalable as project grows
- ✅ Different speeds for different needs
- ✅ Professional test structure

---

## 🔧 Common Commands

```bash
# Run all backend tests
python -m pytest tests/backend/ -v

# Run only unit tests (super fast)
python -m pytest tests/backend/unit/ -v

# Run integration tests
python -m pytest tests/backend/integration/ -v

# Run end-to-end tests
python -m pytest tests/backend/e2e/ -v

# Run specific test file
python tests/backend/unit/test_jwt_standalone.py

# Run with output details
python -m pytest tests/backend/ -v -s

# Run with coverage
python -m pytest tests/backend/ --cov=app --cov-report=html
```

---

## 📚 Related Documentation

- **[Backend Tests Guide](./backend/README.md)**
- **[Unit Tests](./backend/unit/README.md)**
- **[Integration Tests](./backend/integration/README.md)**
- **[E2E Tests](./backend/e2e/README.md)**
- **[Main Project README](../README.md)**
- **[API Documentation](../docs/api/)**

---

## 🤝 Contributing Tests

When adding new tests:

1. **Determine Test Type**
   - Unit: Single component, no dependencies
   - Integration: Multiple components
   - E2E: Full workflows

2. **Place in Correct Folder**
   - Unit tests → `tests/backend/unit/`
   - Integration tests → `tests/backend/integration/`
   - E2E tests → `tests/backend/e2e/`

3. **Follow Naming Convention**
   - `test_<feature>.py`
   - Clear test function names
   - Comprehensive docstrings

4. **Keep Tests Fast**
   - Use mocks for slow operations
   - Use in-memory databases
   - Test one thing per test

---

## 📞 Support

For test-related issues:
1. Check test output for error messages
2. Review test file docstrings
3. Check [API Documentation](../docs/api/)
4. Review [Setup Guide](../docs/getting-started/SETUP_GUIDE.md)

---

**Last Updated:** April 3, 2026  
**Status:** ✅ All 6 tests organized and ready

🚀 Happy testing! 🧪
