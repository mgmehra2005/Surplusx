# 🧪 Testing Documentation

Complete guide to SurplusX testing framework, test organization, and how to run tests.

---

## 📁 Structure

```
docs/testing/
├── README.md                   # Testing overview (this file)
└── TEST_ORGANIZATION.md        # How tests are organized
```

---

## 🎯 Quick Start

### Run All Tests
```bash
cd tests/backend
python -m pytest . -v
```

### Run by Category
```bash
# Unit tests (fast - <1s)
python tests/backend/unit/test_jwt_standalone.py

# Integration tests (~2s)
python tests/backend/integration/test_jwt_db_integration.py

# E2E tests (full system - ~5s)
python tests/backend/e2e/SYSTEM_TEST.py
```

---

## 📊 Test Organization

Tests are organized by scope and speed:

| Type | Location | Count | Speed |
|------|----------|-------|-------|
| **Unit** | `tests/backend/unit/` | 2 | ⚡ <1s |
| **Integration** | `tests/backend/integration/` | 2 | ⚡ ~2s |
| **E2E** | `tests/backend/e2e/` | 2 | 🐢 ~5s |

See [TEST_ORGANIZATION.md](./TEST_ORGANIZATION.md) for detailed breakdown.

---

## 🧬 Test Files

### Unit Tests (Isolated Components)
- `test_jwt_standalone.py` - JWT token generation & validation
- `test_auth_service_bugs.py` - Auth service functions

### Integration Tests (Component Interaction)
- `test_jwt_db_integration.py` - JWT + Database together
- `test_jwt.py` - JWT workflow

### E2E Tests (Full System)
- `SYSTEM_TEST.py` - 7 comprehensive system tests
- `test_auth_bugs_fixed.py` - Auth bug fixes validation

---

## ✅ Test Coverage

| Component | Coverage | Status |
|-----------|----------|--------|
| **Authentication** | Register, login, JWT | ✅ |
| **API Endpoints** | CRUD operations | ✅ |
| **Database** | Models, persistence | ✅ |
| **AI Services** | Freshness scoring | ✅ |
| **Frontend** | Integration layer | ✅ |

---

## 📝 Documentation Files

- **[TEST_ORGANIZATION.md](./TEST_ORGANIZATION.md)** - Complete test organization guide
- See [tests/README.md](../../tests/README.md) for additional test documentation

---

## 🚀 Pre-Deployment Checklist

Run before deploying to production:

```bash
# 1. Unit tests (fast validation)
python tests/backend/unit/*.py

# 2. Integration tests
python tests/backend/integration/*.py

# 3. Full system test
python tests/backend/e2e/SYSTEM_TEST.py

# Expected result:
# ✅ All tests passed! System is ready.
```

---

## 🔗 Related

- [Main Tests Guide](../../tests/README.md)
- [Backend Tests Overview](../../tests/backend/README.md)
- [Getting Started](../getting-started/SETUP_GUIDE.md)
- [Main Documentation](../README.md)

---

**Location:** `docs/testing/`  
**Status:** ✅ Ready  
**Last Updated:** April 3, 2026
