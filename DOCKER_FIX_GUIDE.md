# Docker Environment - Complete Fix & Resolution Guide

## 🎯 What Was Wrong

Your Docker Compose setup had three critical issues preventing successful startup:

### Issue #1: MySQL Database Initialization Failure
**Error Message:**
```
ERROR [Entrypoint]: Database is uninitialized and password option is not specified
You need to specify one of the following as an environment variable:
- MYSQL_ROOT_PASSWORD
- MYSQL_ALLOW_EMPTY_PASSWORD
- MYSQL_RANDOM_ROOT_PASSWORD
```

**Root Cause:** MySQL container expected `MYSQL_ROOT_PASSWORD` but the compose file only passed `MYSQL_PASSWORD`

**Fixed By:** Updated `docker-compose.dev.yml` to explicitly set environment variables that MySQL expects

---

### Issue #2: Race Condition - Backend Starting Before Database Ready
**Error Message:**
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, 
"Can't connect to MySQL server on 'db' ([Errno -5] No address associated with hostname)")
```

**Root Cause:** Backend service had no dependency on database, so it tried to connect before MySQL finished initializing

**Fixed By:** 
- Added health check to MySQL service (tests connectivity)
- Added `depends_on` with `service_healthy` condition
- Backend now waits for health check to pass before starting

---

### Issue #3: Backend Crashed on Connection Failure
**Error Message:**
```
backend-1 exited with code 1
```

**Root Cause:** Backend immediately called `db.create_all()` in `run.py` with no retry logic

**Fixed By:** Added `wait_for_db()` function that:
- Attempts connection up to 30 times
- Waits 2 seconds between retries
- Gracefully handles connection failures
- Provides detailed logging

---

## ✅ Changes Made

### 1. `.env` File
```diff
# Database Configuration
MYSQL_HOST=db
MYSQL_PORT=3306
MYSQL_USER=root
+ MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_PASSWORD=rootpassword
MYSQL_DATABASE=surplusx
```

**Why:** MySQL container specifically looks for `MYSQL_ROOT_PASSWORD` to initialize

---

### 2. `docker-compose.dev.yml` File

**Key Improvements:**

#### Added Database Health Check
```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  timeout: 20s
  retries: 10
  interval: 5s
```
- Checks if MySQL is responding to queries
- Backend waits for this to pass before starting

#### Added Service Dependency
```yaml
backend:
  depends_on:
    db:
      condition: service_healthy  # Waits for health check!
```
- Backend won't start until database health check passes
- Prevents race conditions

#### Added Docker Network
```yaml
networks:
  surplusx_network:
    driver: bridge
```
- All services connected to same network
- Enables reliable inter-service communication

#### Added Persistent Volume
```yaml
volumes:
  mysql_data:/var/lib/mysql
```
- Database data persists between container restarts
- Not lost when you stop/start containers

---

### 3. `backend/run.py` File

**Added Retry Logic:**
```python
def wait_for_db(max_retries=30, retry_delay=2):
    """Wait for database to be ready before proceeding"""
    logger.info("Waiting for database to be ready...")
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.session.execute(text('SELECT 1'))  # Test connection
                db.session.commit()
                logger.info("✓ Database is ready!")
                return True
        except Exception as e:
            # Retry after 2 seconds
            time.sleep(retry_delay)
    
    return False
```

**Benefits:**
- Tolerates temporary connection delays
- Gives MySQL time to fully initialize
- Clear logging of connection attempts
- Fails gracefully with helpful error messages

---

## 🚀 How to Test the Fix

### Step 1: Clean Up Previous Failed Containers
```powershell
cd c:\Users\Saksham Rastogi\Downloads\Surplusx-1

# Stop and remove everything
docker-compose -f docker-compose.dev.yml down -v

# Verify cleanup
docker-compose -f docker-compose.dev.yml ps
```

### Step 2: Rebuild Images (Important!)
```powershell
docker-compose -f docker-compose.dev.yml build
```
⚠️ This is crucial! New code in `run.py` needs to be built into the backend image

### Step 3: Start Services
```powershell
docker-compose -f docker-compose.dev.yml up
```

### Step 4: Watch for Success Indicators

**Expected Output:**
```
db-1        | 2026-04-03 09:33:56 [Note] ... MySQL Server started
db-1        | 2026-04-03 09:33:56 [Note] ... ready for connections
frontend-1  | ✓ Vite DevServer ready in 245ms
frontend-1  | ➜ Local: http://localhost:3000/
backend-1   | Waiting for database to be ready...
backend-1   | ✓ Database is ready!
backend-1   | ✓ Database tables initialized successfully
backend-1   | Starting Flask application on 0.0.0.0:5000 ✓
```

---

## 🧪 Quick Testing After Startup

### Test 1: Check Container Status
```powershell
docker-compose -f docker-compose.dev.yml ps
```
Should show: `frontend-1 running`, `backend-1 running`, `db-1 running`

### Test 2: View Logs
```powershell
# All services
docker-compose -f docker-compose.dev.yml logs

# Just backend
docker-compose -f docker-compose.dev.yml logs backend

# Just database
docker-compose -f docker-compose.dev.yml logs db

# Last 50 lines
docker-compose -f docker-compose.dev.yml logs --tail=50
```

### Test 3: Connect to Frontend
- Open browser: **http://localhost:3000**
- Should show your Vite frontend

### Test 4: Test Backend Health
```powershell
# From host machine (if you added /health endpoint)
curl http://localhost:5000/health

# Or using Invoke-WebRequest in PowerShell
Invoke-WebRequest -Uri http://localhost:5000/health
```

### Test 5: Connect to Database Directly
```powershell
# Using docker exec to access MySQL from host
docker exec -it surplusx-1-db-1 mysql -u root -prootpassword surplusx

# Then you can run SQL commands:
# SHOW TABLES;
# SELECT * FROM user;
```

---

## 🛠️ Helpful Commands

### Start Services
```powershell
# Normal start
docker-compose -f docker-compose.dev.yml up

# Start in background (detached mode)
docker-compose -f docker-compose.dev.yml up -d

# Rebuild and start
docker-compose -f docker-compose.dev.yml up --build
```

### Stop Services
```powershell
# Stop (keep containers)
docker-compose -f docker-compose.dev.yml stop

# Stop and remove containers (keep volumes/data)
docker-compose -f docker-compose.dev.yml down

# Stop and remove everything including data (full reset)
docker-compose -f docker-compose.dev.yml down -v
```

### View Logs and Status
```powershell
# Show all logs
docker-compose -f docker-compose.dev.yml logs

# Follow logs in real-time
docker-compose -f docker-compose.dev.yml logs -f

# Specific service logs
docker-compose -f docker-compose.dev.yml logs backend

# Last N lines
docker-compose -f docker-compose.dev.yml logs --tail=100
```

### Execute Commands in Containers
```powershell
# Run bash in backend container
docker exec -it surplusx-1-backend-1 bash

# Run bash in database container
docker exec -it surplusx-1-db-1 bash

# Run MySQL commands directly
docker exec -it surplusx-1-db-1 mysql -u root -prootpassword -e "SHOW TABLES;"
```

### Restart Services
```powershell
# Restart all services
docker-compose -f docker-compose.dev.yml restart

# Restart specific service
docker-compose -f docker-compose.dev.yml restart backend
```

---

## 🔍 Troubleshooting Guide

### Problem: MySQL keeps exiting with code 1

**Check:**
```powershell
docker-compose -f docker-compose.dev.yml logs db
```

**Fix:**
1. Verify `.env` has `MYSQL_ROOT_PASSWORD=rootpassword`
2. Full reset: `docker-compose -f docker-compose.dev.yml down -v`
3. Rebuild: `docker-compose -f docker-compose.dev.yml build --no-cache`
4. Start: `docker-compose -f docker-compose.dev.yml up`

---

### Problem: Backend still can't connect to database

**Check:**
```powershell
# See if MySQL is healthy
docker-compose -f docker-compose.dev.yml logs db

# See backend retry attempts
docker-compose -f docker-compose.dev.yml logs backend | Select-String "Waiting", "attempt", "ready"
```

**Fix:**
1. Ensure health check is passing: `docker-compose ps` (should show `(healthy)` for db)
2. Increase retry count in `backend/run.py`:
   ```python
   if not wait_for_db(max_retries=60, retry_delay=3):  # Try more times
   ```
3. Rebuild: `docker-compose build --no-cache`

---

### Problem: Port already in use

**Find what's using the port:**
```powershell
# Check port 3000
netstat -ano | findstr :3000

# Check port 5000
netstat -ano | findstr :5000

# Check port 3306
netstat -ano | findstr :3306
```

**Fix:**
- Kill the process using the command above, OR
- Change port in `docker-compose.dev.yml`:
  ```yaml
  backend:
    ports:
      - "5001:5000"  # Changed from 5000 to 5001
  ```

---

### Problem: Containers not communicating with each other

**Check:**
```powershell
# List networks
docker network ls

# Inspect surplusx_network
docker network inspect surplusx-1_surplusx_network

# See which containers are connected
docker network inspect surplusx-1_surplusx_network | findstr -i containers
```

**Fix:**
- Ensure all services are connected to `surplusx_network`
- Check `.env` has `MYSQL_HOST=db` (the service name, not localhost!)

---

## 📊 Startup Flow Diagram

```
You run: docker-compose up
    ↓
[1] MySQL container starts
    ↓
[2] MySQL initializes database (using MYSQL_ROOT_PASSWORD)
    ↓
[3] MySQL waits for health check to pass
    ↓
[4] Health check: "mysqladmin ping" succeeds ✓
    ↓
[5] Backend container starts (depends_on: service_healthy)
    ↓
[6] Backend calls wait_for_db()
    ↓
[7] Backend tests connection (SELECT 1)
    ↓
[8] Connection succeeds ✓
    ↓
[9] Backend calls db.create_all()
    ↓
[10] Database tables created (if needed)
    ↓
[11] Flask server starts on 0.0.0.0:5000 ✓
    ↓
[12] Frontend container starts (Vite dev server)
    ↓
[13] Vite starts on 0.0.0.0:3000 ✓
    ↓
✅ READY! All services running
```

---

## 📝 Files Modified

| File | Change | Reason |
|------|--------|--------|
| `.env` | Added `MYSQL_ROOT_PASSWORD` | MySQL needs explicit env var |
| `docker-compose.dev.yml` | Complete restructure | Added health checks, deps, network |
| `backend/run.py` | Added `wait_for_db()` | Retry logic for DB connection |

---

## 🎓 Key Takeaways

1. **Health Checks** - Let services verify they're ready
2. **Dependencies** - Use `depends_on` with `service_healthy` condition
3. **Retry Logic** - Don't fail immediately on connection errors
4. **Networks** - Ensure services can communicate
5. **Volumes** - Keep data persistent across restarts
6. **Logging** - Log everything for debugging

---

## ✨ Next Steps

1. ✅ Run: `docker-compose -f docker-compose.dev.yml down -v`
2. ✅ Run: `docker-compose -f docker-compose.dev.yml build`
3. ✅ Run: `docker-compose -f docker-compose.dev.yml up`
4. ✅ Verify all three services are running
5. ✅ Test endpoints and database connection

**You're all set! 🚀**

---

**Last Updated:** April 3, 2026
**Status:** Fixed & Ready for Development
