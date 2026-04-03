# SurplusX - Setup & Development Guide

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- MySQL 8.0 (or use Docker)
- Docker & Docker Compose (optional)

---

## 🐳 Option 1: Development with Docker Compose

### Start Development Environment
```bash
# Navigate to project root
cd Surplusx-1

# Copy environment file
cp .env.example .env

# Start all services
docker-compose -f docker-compose.dev.yml up --build

# Services will be available at:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# MySQL: localhost:3308
```

### Stop Services
```bash
docker-compose -f docker-compose.dev.yml down
```

---

## 🖥️ Option 2: Local Development (Non-Docker)

### Backend Setup

#### 1. Create Python Virtual Environment
```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
cd ..
cp .env.example .env

# Edit .env and set:
# MYSQL_HOST=localhost
# MYSQL_USER=your_db_user
# MYSQL_PASSWORD=your_db_password
```

#### 4. Create Database
```bash
mysql -u root -p

# In MySQL CLI:
CREATE DATABASE surplusx;
CREATE USER 'surplusx_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON surplusx.* TO 'surplusx_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 5. Run Backend
```bash
cd backend
python run.py

# Server runs at http://localhost:5000
# Database tables auto-created on startup ✓
```

### Frontend Setup

#### 1. Install Dependencies
```bash
cd frontend
npm install --legacy-peer-deps --no-audit
```

#### 2. Configure Environment
```bash
# Frontend auto-detects based on vite.config.js
# Default: http://localhost:5000/api
```

#### 3. Start Development Server
```bash
npm run dev

# Frontend runs at http://localhost:3000
```

---

## 📝 Test User Accounts

### After system is running, register test users:

#### Donor User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@example.com",
    "name": "John Donor",
    "password": "SecurePass123!",
    "role": "DONOR"
  }'
```

#### NGO User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ngo@example.com",
    "name": "Help NGO",
    "password": "SecurePass123!",
    "role": "NGO"
  }'
```

#### Admin User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "name": "John Admin",
    "password": "SecurePass123!",
    "role": "ADMIN"
  }'
```

---

## 🔐 Testing Authentication

### 1. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "donor@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "uid": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Donor",
    "email": "donor@example.com",
    "role": "DONOR"
  }
}
```

### 2. Save Token
```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 🍲 Testing Food Operations

### 1. Add Food Item
```bash
curl -X POST http://localhost:5000/api/food/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Rice Packets",
    "food_type": "prepared",
    "quantity": 10,
    "quantity_unit": "units",
    "preparation_date": "2026-04-03T15:00:00",
    "expiry_date": "2026-04-04T15:00:00",
    "description": "Cooked rice packets in clean containers"
  }'
```

### 2. List Available Food
```bash
curl -X GET "http://localhost:5000/api/food?status=AVAILABLE" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Get Specific Food Item
```bash
curl -X GET http://localhost:5000/api/food/{food_id} \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Update Food Item
```bash
curl -X PUT http://localhost:5000/api/food/{food_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "MATCHED",
    "quantity": 5
  }'
```

### 5. Delete Food Item
```bash
curl -X DELETE http://localhost:5000/api/food/{food_id} \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Frontend Testing

1. **Open** http://localhost:3000
2. **Register** a new account with valid credentials
3. **Login** with registered credentials
4. **View Dashboard** based on role (donor/ngo/admin)
5. **Add Food Item** (donor only)
6. **View Available Food** (NGO)
7. **Claim Food** (NGO)

---

## 🔍 Troubleshooting

### Backend Won't Start

**Error:** "Connection refused on port 5000"
- Check if backend is running: `lsof -i :5000`
- Kill existing process: `lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9`

**Error:** "Database connection failed"
- Check MySQL is running: `mysql -u root -p`
- Verify credentials in `.env`
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

**Error:** "JWT_SECRET_KEY not found"
- Ensure `.env` has `JWT_SECRET_KEY` set
- Restart backend server after changes

### Frontend Won't Connect

**Error:** "API calls fail with CORS error"
- Check backend CORS config in `.env`: `ORIGINS=http://localhost:3000`
- Restart backend server
- Clear browser cache or open in incognito mode

**Error:** "Blank page or app not loading"
- Check console for errors: Press F12 in browser
- Clear node_modules: `rm -rf node_modules && npm install --legacy-peer-deps`
- Restart dev server: `npm run dev`

### Database Issues

**Error:** "Tables not created"
- Tables auto-create on backend startup
- Check logs: "✓ Database tables initialized"
- Manually create: `python -c "from app import app, db; app.app_context().push(); db.create_all()"`

---

## 📚 Project Structure

```
Surplusx-1/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── api_gateway/       # API routes (auth, food, etc.)
│   │   ├── auth_service/      # Auth logic
│   │   ├── ai_service/        # Freshness scoring
│   │   └── db_models/         # Database models
│   ├── requirements.txt       # Python dependencies
│   ├── config.py             # Configuration
│   └── run.py                # Entry point
├── frontend/                  # React app
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── context/         # React context (auth)
│   │   ├── services/        # API client (★ now calls real API)
│   │   └── App.jsx          # Router
│   └── package.json         # JavaScript dependencies
├── docker-compose.yml       # Production compose
├── docker-compose.dev.yml   # Development compose
├── .env                     # Environment variables
├── .env.example             # Environment template
└── FIXES_SUMMARY.md        # This summary ★
```

---

## 🚀 Production Deployment

### Before Deploying:

1. **Change Secrets**
   ```bash
   # Generate new secrets
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   - Update `SECRET_KEY` in `.env`
   - Update `JWT_SECRET_KEY` in `.env`

2. **Use Database Backup**
   - Don't use development credentials
   - Create dedicated database user with limited privileges

3. **Enable HTTPS**
   - Get SSL certificates (Let's Encrypt)
   - Update frontend API URL to HTTPS

4. **Configure Logging**
   - Set `LOG_LEVEL=WARNING` in production
   - Configure log aggregation

5. **Add Monitoring**
   - Set up error tracking (Sentry)
   - Set up performance monitoring

### Deployment Commands

```bash
# Build frontend
cd frontend
npm run build

# Deploy with Docker Compose
docker-compose up --build -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## 📞 Support

For issues or questions:
1. Check FIXES_SUMMARY.md for fixes applied
2. Check backend logs: `docker-compose logs backend`
3. Check frontend console: Browser DevTools (F12)
4. Enable debug mode: Set `DEBUG=True` in backend config

---

**Status:** ✅ Ready for Development
**Last Updated:** April 3, 2026
