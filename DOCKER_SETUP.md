# Docker Setup & Troubleshooting Guide

## Issues Fixed

### 1. ✅ MySQL Environment Variable Mismatch
**Problem:** MySQL container expects `MYSQL_ROOT_PASSWORD` but was receiving `MYSQL_PASSWORD`
**Solution:** Updated `docker-compose.dev.yml` to explicitly set `MYSQL_ROOT_PASSWORD` environment variable

### 2. ✅ No Service Dependency Management
**Problem:** Backend was starting before MySQL service was ready, causing connection failures
**Solution:** 
- Added `depends_on` with `service_healthy` condition
- Added health check to MySQL service
- MySQL must pass health check before backend starts

### 3. ✅ No Retry Logic in Backend
**Problem:** Backend crashed immediately if database wasn't ready
**Solution:** Added `wait_for_db()` function in `run.py` that:
- Attempts connection up to 30 times
- Waits 2 seconds between retries
- Logs detailed progress
- Only starts Flask if connection successful

### 4. ✅ Missing Docker Network & Volumes
**Problem:** Containers on different networks, no persistent data
**Solution:**
- Created `surplusx_network` for inter-service communication
- Added named volume `mysql_data` for persistent database
- All services connected to same network

---

## Quick Start

### First Time Setup (Clean Start)

```bash
# 1. Navigate to project root
cd "c:\Users\Saksham Rastogi\Downloads\Surplusx-1"

# 2. Clean up any existing containers/volumes
docker-compose -f docker-compose.dev.yml down -v

# 3. Rebuild images (important after code changes)
docker-compose -f docker-compose.dev.yml build

# 4. Start services
docker-compose -f docker-compose.dev.yml up
```

### Subsequent Starts

```bash
# Simple start (no rebuild needed unless dependencies changed)
docker-compose -f docker-compose.dev.yml up
```

### Stopping Services

```bash
# Stop without removing containers
docker-compose -f docker-compose.dev.yml stop

# Stop and remove containers (keeps volumes)
docker-compose -f docker-compose.dev.yml down

# Stop, remove everything including volumes (full reset)
docker-compose -f docker-compose.dev.yml down -v
```

---

## Health Checks

### Check Service Status

```bash
# See all running containers
docker-compose -f docker-compose.dev.yml ps

# View logs for all services
docker-compose -f docker-compose.dev.yml logs

# View logs for specific service
docker-compose -f docker-compose.dev.yml logs backend
docker-compose -f docker-compose.dev.yml logs db
docker-compose -f docker-compose.dev.yml logs frontend
```

### Database Connection Tests

```bash
# Connect to MySQL from host (if MySQL client installed)
mysql -h localhost -P 3306 -u root -p
# When prompted for password, enter: rootpassword

# Or use docker exec
docker exec -it surplusx-1-db-1 mysql -user=root -prootpassword surplusx
```

### Test Frontend
- Open browser: http://localhost:3000

### Test Backend
- Vite should be running on http://localhost:5000/health (if health endpoint exists)
- Check logs: `docker-compose logs backend`

---

## Expected Startup Sequence

When you run `docker-compose -f docker-compose.dev.yml up`, you should see:

```
frontend-1 | ✓ Vite dev server ready
db-1       | ✓ MySQL ready (health check pass)
backend-1  | Waiting for database to be ready...
backend-1  | ✓ Database is ready!
backend-1  | ✓ Database tables initialized successfully
backend-1  | Flask application on 0.0.0.0:5000
```

---

## Troubleshooting

### Issue: MySQL keeps crashing
```
db-1 exited with code 1
```
**Solution:** 
- Ensure `.env` has `MYSQL_ROOT_PASSWORD=rootpassword`
- Run: `docker-compose -f docker-compose.dev.yml down -v`
- Then: `docker-compose -f docker-compose.dev.yml up --build`

### Issue: Backend can't connect to database
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'db'")
```
**Solution:**
- Check MySQL logs: `docker-compose logs db`
- Check backend is waiting for db: `docker-compose logs backend`
- Increase `max_retries` or `retry_delay` in `backend/run.py` if needed
- Ensure health check is passing: `docker-compose logs db | grep -i health`

### Issue: Port already in use
```
Error response from daemon: Ports are not available
```
**Solution:**
- Kill existing process: `lsof -i :3000` or `lsof -i :5000` or `lsof -i :3306`
- Or change ports in `docker-compose.dev.yml`

### Issue: Containers start but don't stay running
**Solution:**
- Check logs: `docker-compose -f docker-compose.dev.yml logs`
- Look for error messages in specific service logs
- Make sure `.env` file has all required variables

---

## Configuration Files Changed

### `.env`
- Added `MYSQL_ROOT_PASSWORD=rootpassword` (MySQL needs this)

### `docker-compose.dev.yml`
- Reorganized service order (db first)
- Added health check to MySQL
- Added `depends_on` with service_healthy condition
- Added custom Docker network: `surplusx_network`
- Added persistent volume: `mysql_data:/var/lib/mysql`

### `backend/run.py`
- Added `wait_for_db()` function
- Added retry logic (30 attempts, 2 second delay)
- Better logging for startup process
- Only starts Flask if database connection successful

---

## Files Reference

**docker-compose.dev.yml** - Development environment orchestration
- MySQL with health checks
- Backend with database dependency
- Frontend with dev server
- Shared network and volumes

**.env** - Environment variables
- Database credentials
- Flask configuration
- CORS settings
- JWT secrets

**backend/run.py** - Application entry point
- Database connection retry logic
- Table initialization
- Flask startup

---

## Next Steps

1. ✅ Run: `docker-compose -f docker-compose.dev.yml up`
2. ✅ Verify all containers are healthy
3. ✅ Test API endpoints
4. ✅ Test frontend on localhost:3000
5. ✅ Check database: `docker exec -it surplusx-1-db-1 mysql -u root -prootpassword`

---

**Last Updated:** April 3, 2026
**Status:** Ready for Development
