# 🧪 TESTING GUIDE - ALL FIXES

## Backend Tests

### 1. Health Check Endpoint
```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/status
```
**Expected:** Both return `200 OK` with database status

---

### 2. Authentication - Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@example.com",
    "name": "John Donor",
    "password": "SecurePassword123",
    "role": "DONOR"
  }'
```
**Expected:** `201 Created` with user data

---

### 3. Authentication - Login & JWT Token
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "donor@example.com",
    "password": "SecurePassword123"
  }'
```
**Expected:** 
```json
{
  "message": "Login successful with email!",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "username": "donor@example.com",
  "email": "donor@example.com",
  "role": "DONOR"
}
```

---

### 4. Add Food Item (POST /api/food/add)
```bash
TOKEN="your_jwt_token_here"

curl -X POST http://localhost:5000/api/food/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fresh Tomatoes",
    "description": "Ripe tomatoes from farm",
    "food_type": "raw",
    "quantity": 5,
    "quantity_unit": "kg",
    "preparation_date": "2026-04-02T10:00:00",
    "expiry_date": "2026-04-04T18:00:00",
    "location": {
      "address": "123 Farm Lane",
      "city": "Springfield",
      "state": "IL",
      "zipCode": "62701",
      "country": "USA"
    }
  }'
```
**Expected:** `201 Created` with food_id, freshness_score

---

### 5. Get All Foods (GET /api/food)
```bash
curl http://localhost:5000/api/food?status=AVAILABLE&limit=10
```
**Expected:** `200 OK` with array of foods, pagination info

---

### 6. Get Single Food (GET /api/food/{id})
```bash
curl http://localhost:5000/api/food/food_id_here
```
**Expected:** `200 OK` with single food details

---

### 7. Update Food Item (PUT /api/food/{id})
```bash
TOKEN="your_jwt_token_here"

curl -X PUT http://localhost:5000/api/food/food_id_here \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "MATCHED",
    "quantity": 3
  }'
```
**Expected:** `200 OK` with updated food data

---

### 8. Delete Food Item (DELETE /api/food/{id})
```bash
TOKEN="your_jwt_token_here"

curl -X DELETE http://localhost:5000/api/food/food_id_here \
  -H "Authorization: Bearer $TOKEN"
```
**Expected:** `200 OK` with success message

---

## Frontend Tests

### 1. User Registration
- Navigate to registration page
- Fill in: email, name, password, confirm password
- Click register
- **Expected:** User created, redirected to login

---

### 2. User Login
- Enter email/username and password
- Click login
- **Expected:** 
  - JWT token stored in localStorage
  - Redirected to dashboard
  - Token visible in browser DevTools → Application → LocalStorage → `surplusx-auth`

---

### 3. Add Food Item
- Navigate to Donor Dashboard
- Fill all form fields:
  - Food name
  - Food type (prepared/raw/packaged/baked)
  - Quantity
  - Unit
  - Preparation date (paste)
  - Expiry date (in future)
  - Description
  - Location
- Click "Add Food"
- **Expected:** 
  - Confirmation modal appears
  - After confirmation, food added to list
  - Toast message: "Food item added successfully"

---

### 4. View Available Foods
- Navigate to Available Foods page
- **Expected:**
  - Foods display with freshness scores
  - Can filter by food type
  - Pagination works
  - Each food shows: title, description, quantity, unit, expiry date

---

### 5. Claim Food Item
- On Available Foods page
- Click "Claim" on a food item
- **Expected:** Status changes to MATCHED, item removed from available list

---

### 6. Update Food Item
- On My Donations page
- Click "Edit" on a food item
- Change quantity or status
- Click "Save"
- **Expected:** 
  - Changes saved
  - Item updates in list
  - Toast: "Food item updated successfully"

---

### 7. Delete Food Item
- On My Donations page
- Click "Delete" on a food item
- Confirm deletion
- **Expected:**
  - Item removed from list
  - Toast: "Food item deleted successfully"

---

## Security Tests

### 1. JWT Token Validation
- Logout (clear localStorage)
- Try to access protected endpoint without token
- **Expected:** `401 Unauthorized`

### 2. Ownership Verification
- User A creates food item
- User B tries to update User A's item
- **Expected:** `403 Forbidden` - "You can only update your own listings"

### 3. Password Not in Response
- Login and capture response
- Check response contains: token, username, email, role
- Check response DOES NOT contain: password, password_hash, uid
- **Expected:** No sensitive data leakage

---

## Database Tests

### 1. Freshness Score Storage
- Add food item
- Query database: `SELECT title, freshness_score FROM food_listings`
- **Expected:** freshness_score value between 0-1

### 2. Food Type Enum
- Add food with invalid type: "VEGETABLES"
- **Expected:** `400 Bad Request` - "Invalid food type"

### 3. Date Validation
- Try expiry_date before preparation_date
- **Expected:** `400 Bad Request` - "Expiry date must be after preparation date"

---

## Command Line Test Script

```bash
#!/bin/bash

BASE_URL="http://localhost:5000/api"

# Test 1: Register
echo "🔐 Registering user..."
REGISTER=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "Test123!",
    "role": "DONOR"
  }')
echo $REGISTER

# Test 2: Login
echo -e "\n🔑 Logging in..."
LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "Test123!"
  }')
TOKEN=$(echo $LOGIN | grep -o '"token":"[^"]*' | cut -d'"' -f4)
echo "Token: $TOKEN"

# Test 3: Add Food
echo -e "\n🍅 Adding food item..."
FOOD=$(curl -s -X POST $BASE_URL/food/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Tomatoes",
    "description": "Fresh tomatoes",
    "food_type": "raw",
    "quantity": 5,
    "quantity_unit": "kg",
    "preparation_date": "2026-04-02T10:00:00",
    "expiry_date": "2026-04-04T18:00:00",
    "location": {"address": "123 St", "city": "Test City"}
  }')
echo $FOOD

# Test 4: Get Foods
echo -e "\n📋 Getting all foods..."
curl -s -X GET "$BASE_URL/food?status=AVAILABLE" | jq

# Test 5: Health Check
echo -e "\n❤️ Health check..."
curl -s -X GET $BASE_URL/health | jq
```

---

## Expected Results Summary

| Test | Expected Status | Notes |
|------|-----------------|-------|
| Health check | 200 | DB connected |
| Register | 201 | User created |
| Login | 200 | Token included |
| Add food | 201 | ID + freshness_score |
| Get foods | 200 | Pagination included |
| Get single | 200 | Full details |
| Update | 200 | Changes applied |
| Delete | 200 | Item removed |
| Invalid type | 400 | Error msg |
| Invalid date | 400 | Error msg |
| No token | 401 | Unauthorized |
| Wrong owner | 403 | Forbidden |

