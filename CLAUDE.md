# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SurplusX is a full-stack platform for managing food surplus between donors and NGOs. The application enables donors to list surplus food, NGOs to claim it, and administrative oversight for the entire system.

## Tech Stack

### Frontend
- **React 19** with React Router for navigation
- **Vite** as build tool and dev server
- **Tailwind CSS** for styling
- **Axios** for API calls
- Port: 3000 (dev), served via nginx (production)

### Backend
- **Flask** with Blueprint architecture
- **MySQL 8.0** for database
- **Flask-CORS** for cross-origin requests
- Port: 5000

### Containerization
- **Docker** with multi-stage builds
- **docker-compose** for orchestration

## Development Commands

### Frontend Development
```bash
cd frontend
npm install --legacy-peer-deps --no-audit  # Use legacy peer deps per Dockerfile
npm run dev           # Run Vite dev server
npm run build         # Production build
npm run lint          # Run ESLint
npm start            # Alternative dev command (exposed externally)
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python run.py        # Run Flask on localhost:5000
```

### Database
```bash
# MySQL runs on port 3308 (external), 3306 (internal)
# Credentials in .env file
```

### Docker Commands
```bash
# Development (includes frontend and backend)
docker-compose -f docker-compose.dev.yml up --build

# Production (backend + database only - frontend served separately)
docker-compose up --build
```

## Application Architecture

### Backend Structure
The Flask backend uses Blueprints for route organization:

```
backend/
├── app/
│   ├── __init__.py              # App factory and CORS setup
│   ├── api_gateway/             # Main API routes
│   │   ├── auth_routes.py       # Authentication endpoints
│   │   └── food_routes.py       # Food item endpoints
│   ├── auth_service/            # Auth utilities
│   │   └── hashing.py          # Password hashing
│   └── ai_service/              # AI features
│       └── freshnessScore.py   # Food freshness calculation
├── config.py                   # Environment configs
├── requirements.txt
└── run.py                      # Entry point
```

**Key patterns:**
- Routes registered in `app/__init__.py` via blueprints
- All API routes prefixed with `/api/*`
- Configurations vary by environment (development/production)

### Frontend Structure
```
frontend/
├── src/
│   ├── components/              # Reusable components
│   │   ├── Navbar.jsx
│   │   └── ProtectedRoute.jsx  # Role-based route guard
│   ├── context/                 # React Context API
│   │   └── AuthContext.jsx      # Authentication state
│   ├── hooks/                   # Custom React hooks
│   │   └── useAuth.js
│   ├── pages/                   # Page components
│   │   ├── AuthPage.jsx        # Login/register
│   │   ├── LandingPage.jsx
│   │   ├── DonorDashboard.jsx
│   │   ├── NGODashboard.jsx
│   │   └── AdminPanel.jsx
│   ├── services/                # API calls
│   │   └── api.js
│   ├── App.jsx                 # Root router
│   └── main.jsx                # React bootstrap
├── Dockerfile                  # Multi-stage build
└── vite.config.js
```

**Key patterns:**
- Role-based routing with `ProtectedRoute` component
- Auth state managed via Context API and localStorage
- Role assignment based on email pattern (email includes "admin" → admin, "ngo" → ngo, else donor)
- Uses email instead of user IDs

### Authentication Flow
1. Users register/login with username, email, password
2. Role determined by email pattern:
   - Contains "admin" → admin role
   - Contains "ngo" → ngo role
   - Otherwise → donor role
3. Auth state stored in localStorage as `surplusx-auth`
4. Protected routes verify role before rendering

### API Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/food/add` - Add food item (calculates freshness score)

### Database
- **Host**: Configured via environment variables (DB_HOST)
- **Port**: 3308 (external access), 3306 (container internal)
- **Credentials**: DB_USER, DB_PASSWORD, DB_NAME from environment
- **TODO**: Database schema and migration system not yet implemented

## Configuration

Environment variables for both frontend and backend:

```bash
# Backend (.env)
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=surplusx
ORIGINS=http://localhost:3000

# Frontend automatically uses REACT_APP_API_URL=http://localhost:5000/api in dev
```

## Key Development Notes

1. **Always use legacy-peer-deps** when installing npm packages to avoid dependency conflicts
2. **Test with all three roles**: Register with emails containing "admin", "ngo", and regular patterns to test all dashboard experiences
3. **CORS origin**: Backend only allows requests from configured origins (default: http://localhost:3000)
4. **AI Service**: The `freshnessScore.py` calculates food freshness based on preparation time, integrated in food routes
5. **Docker context**: When building Docker images, ensure you're in the correct directory (frontend/ or backend/)
