# 🍲 SurplusX - Food Surplus Management Platform

> A full-stack platform for managing food surplus between donors and NGOs with administrative oversight.

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)](docs/project/COMPLETION_STATUS.md)
[![Tests](https://img.shields.io/badge/tests-7%2F7%20passing-brightgreen)](SYSTEM_TEST.py)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## 🚀 Quick Start

### 1️⃣ Clone & Setup
```bash
# Clone repository
git clone <repo-url>
cd Surplusx-1

# Copy environment file
cp .env.example .env

# Start with Docker (recommended)
docker-compose -f docker-compose.dev.yml up --build
```

### 2️⃣ Access Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **MySQL:** localhost:3308

### 3️⃣ Create Test Account
Register with email: `donor@example.com` or `ngo@example.com`

---

## 📚 Documentation

All documentation is organized in the **[`docs/` folder](./docs/)**.

### Quick Links
- 🏁 **[Getting Started](./docs/getting-started/)** - Setup & installation
- 🔌 **[API Documentation](./docs/api/)** - Endpoints & fixes
- 📋 **[Project Info](./docs/project/)** - Context & status

**[→ View Complete Documentation](./docs/README.md)**

---

## ⭐ Key Features

✅ **User Authentication**
- JWT-based authentication
- Role-based access control (Donor, NGO, Admin)
- Secure password hashing with bcrypt

✅ **Food Management**
- Create, read, update, delete food listings
- Real-time freshness scoring
- Status tracking (available, matched, delivered)

✅ **Role Dashboards**
- Donor dashboard - List surplus food
- NGO dashboard - Browse & claim food
- Admin dashboard - System overview

✅ **Production Ready**
- Comprehensive error handling
- Input validation on all endpoints
- Automated database initialization
- Complete test coverage (7/7 passing)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask with SQLAlchemy
- **Database:** MySQL 8.0
- **Authentication:** JWT (Flask-JWT-Extended)
- **Password Hashing:** Bcrypt

### Frontend
- **Framework:** React 19
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Routing:** React Router

### DevOps
- **Containerization:** Docker & Docker Compose
- **Environment:** Development & Production configs

---

## 📊 System Status

| Component | Status | Details |
|-----------|--------|---------|
| **Backend API** | ✅ Working | JWT auth, CRUD operations, DB auto-init |
| **Frontend** | ✅ Working | Real API calls, role-based routing |
| **Database** | ✅ Working | Auto-initialized on startup |
| **Authentication** | ✅ Working | JWT tokens, password hashing |
| **Tests** | ✅ Passing | 7/7 system tests passed |

---

## 🎯 What Was Fixed

**15+ Critical Bugs Fixed:**
1. ✅ Registration endpoint disabled → Now fully functional
2. ✅ No JWT tokens → JWT implemented
3. ✅ Hardcoded food data → Dynamic data handling
4. ✅ Frontend mock data → Real API calls
5. ✅ Email-based roles → Database roles
6. ✅ ...and 10+ more

**[→ See Complete Fix List](./docs/api/FIXES_SUMMARY.md)**

---

## 📁 Project Structure

```
Surplusx-1/
├── docs/                           # Documentation
│   ├── README.md                  # Documentation index
│   ├── getting-started/           # Setup guides
│   ├── api/                       # API & technical docs
│   └── project/                   # Project info
├── backend/                        # Flask API
│   ├── app/
│   │   ├── api_gateway/          # Endpoints (auth, food, etc.)
│   │   ├── auth_service/         # Authentication logic
│   │   ├── ai_service/           # Freshness scoring
│   │   └── db_models/            # Database models
│   ├── config.py                 # Configuration
│   ├── run.py                    # Entry point
│   └── requirements.txt          # Dependencies
├── frontend/                       # React app
│   ├── src/
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   ├── services/            # API client
│   │   └── App.jsx              # Router
│   └── package.json             # Dependencies
├── docker-compose.yml           # Production compose
├── docker-compose.dev.yml       # Development compose
├── .env.example                 # Configuration template
├── SYSTEM_TEST.py              # Test suite
└── README.md                    # This file
```

---

## 🚦 Getting Started (Details)

### Option 1: Docker (Recommended)
```bash
docker-compose -f docker-compose.dev.yml up --build
```
**Services:** Backend (5000) | Frontend (3000) | MySQL (3308)

### Option 2: Local Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python run.py

# Frontend (new terminal)
cd frontend
npm install --legacy-peer-deps
npm run dev
```

**[→ Full Setup Guide](./docs/getting-started/SETUP_GUIDE.md)**

---

## 🔐 Authentication

### Register
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123!",
  "role": "DONOR"
}
```

### Login
```bash
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

# Response:
{
  "token": "eyJ0eXAiOiJKV1Q...",
  "user": {
    "uid": "550e8400-e29b-41d4-a716...",
    "name": "John Doe",
    "email": "user@example.com",
    "role": "DONOR"
  }
}
```

**[→ Full API Docs](./docs/api/)**

---

## 🧪 Testing

Run the comprehensive system test:
```bash
cd backend
python SYSTEM_TEST.py
```

**Results:** ✅ 7/7 tests passing

---

## 🤝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with JWT

### Food Operations
- `POST /api/food/add` - Create food listing (donor)
- `GET /api/food` - List all food (filterable by status)
- `GET /api/food/{id}` - Get specific food item
- `PUT /api/food/{id}` - Update food listing (owner only)
- `DELETE /api/food/{id}` - Delete food listing (owner only)

**[→ Complete API Reference](./docs/api/)**

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
# Check port 5000 is not in use
lsof -i :5000

# Verify database connection
mysql -u root -p -e "SHOW DATABASES;"
```

### Frontend not connecting?
```bash
# Clear cache and reinstall
rm -rf frontend/node_modules
cd frontend && npm install --legacy-peer-deps
npm run dev
```

### Database issues?
```bash
# Tables auto-create on startup
# If not working, manually initialize:
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**[→ Full Troubleshooting Guide](./docs/getting-started/SETUP_GUIDE.md)**

---

## 📈 Deployment

### Before Going Live
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Change `JWT_SECRET_KEY` in `.env`
- [ ] Update `ORIGINS` for production domain
- [ ] Set `FLASK_ENV=production`
- [ ] Configure HTTPS

### Deploy with Docker
```bash
docker-compose up --build -d
```

**[→ Production Checklist](./docs/getting-started/SETUP_GUIDE.md)**

---

## 📞 Support

| Issue | Resource |
|-------|----------|
| Setup problems | [Setup Guide](./docs/getting-started/SETUP_GUIDE.md) |
| API questions | [API Docs](./docs/api/) |
| Bug details | [Fixes Summary](./docs/api/FIXES_SUMMARY.md) |
| Project info | [Project Context](./docs/project/PROJECT_CONTEXT.md) |

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🎉 Project Status

**Version:** 1.0  
**Status:** ✅ Production Ready  
**Last Updated:** April 3, 2026  
**All Tests:** ✅ Passing (7/7)  
**All Bugs:** ✅ Fixed (15+)  

---

## 📚 Learn More

- **[Complete Documentation](./docs/README.md)**
- **[Setup Guide](./docs/getting-started/SETUP_GUIDE.md)**
- **[API Documentation](./docs/api/)**
- **[Project Context](./docs/project/PROJECT_CONTEXT.md)**

---

**Ready to use? [Start here →](./docs/README.md)**

Happy coding! 🚀
