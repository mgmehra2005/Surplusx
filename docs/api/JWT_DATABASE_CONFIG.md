# JWT + Database Configuration Guide

## Overview
This guide explains how JWT authentication and the database are configured to work together in the SurplusX backend.

## Architecture

```
User Login Request
        ↓
[Password Verification] ← Database Query
        ↓
[JWT Token Generation] ← Secret Key from Config
        ↓
JWT Token Response
        ↓
Protected Endpoint Request + Token
        ↓
[JWT Decode] ← Secret Key from Config
        ↓
[Database Lookup] ← User ID from Token
        ↓
User Data/Protected Resource
```

## Configuration Files

### 1. `.env` - Environment Variables
```env
# Security
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars!
JWT_SECRET_KEY=your-jwt-secret-key-change-this-min-32-chars!!!
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 hours

# Database
MYSQL_HOST=db              # Docker service name or localhost
MYSQL_PORT=3306            # MySQL port
MYSQL_USER=root            # MySQL user
MYSQL_PASSWORD=rootpassword # MySQL password
MYSQL_DATABASE=surplusx    # Database name

# Application
FLASK_ENV=development      # development, testing, or production
ORIGINS=http://localhost:3000
```

**Important Notes:**
- In production, use strong secret keys (min 32 characters)
- Keep `.env` out of version control (add to `.gitignore`)
- Use different keys for development and production
- Never commit actual secrets to the repository

### 2. `backend/config.py` - Flask Configuration

Defines three configuration classes:

#### Development
- Debug mode enabled
- Full SQL logging
- Less strict validation
- Used by default

#### Testing
- SQLite in-memory database (for CI/CD)
- Test-specific token expiration
- No external database required
- Used for automated testing

#### Production
- Debug mode disabled
- Requires environment variables
- Validates secret key length
- Enables security features

### 3. `backend/app/__init__.py` - Application Initialization

Initialization order is critical:

```python
1. Flask app created
2. App config loaded from config.py
3. SQLAlchemy database initialized
4. JWT Manager initialized
5. CORS configured
6. Routes imported
```

This order ensures:
- Database connection before routes
- JWT keys available before token operations
- Proper error handling throughout

## Database + JWT Integration Points

### Login Flow (POST /api/auth/login)

```python
1. Receive email + password from client
2. Query database: SELECT * FROM users WHERE email = ?
3. Verify password hash
4. Create JWT token with user UID
5. Return token + user data
```

### Protected Endpoint (Headers: Authorization: Bearer <token>)

```python
1. Extract token from Authorization header
2. Decode JWT token using SECRET_KEY
3. Extract user UID from token claims
4. Query database: SELECT * FROM users WHERE uid = ?
5. Return data or 401 if user not found
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-uid-from-database",
    "type": "access",
    "iat": 1234567890,
    "exp": 1234654290
  }
}
```

## How to Deploy

### Local Development with Docker

```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.dev.yml up --build

# Or run with local MySQL
# 1. Start MySQL server
# 2. Update .env with local settings
# 3. Run backend
cd backend
pip install -r requirements.txt
python run.py
```

### Environment Setup

```bash
# Create .env file in project root
cp .env.example .env

# Update .env with your settings
# For development:
FLASK_ENV=development
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password

# For production:
FLASK_ENV=production
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-strong-random-key>
MYSQL_HOST=production-db-host
```

## Testing

### Run All Tests

```bash
# Test JWT authentication
python test_jwt_standalone.py

# Test JWT + Database integration
python test_jwt_db_integration.py
```

### Test Results

- ✅ Password hashing and verification
- ✅ User creation and storage
- ✅ JWT token generation
- ✅ JWT token validation
- ✅ Protected endpoint access
- ✅ Database lookups with JWT user ID

## Security Considerations

### Production Checklist

- [ ] Change all SECRET_KEY values
- [ ] Use HTTPS for all endpoints
- [ ] Enable SQLALCHEMY_ECHO=False
- [ ] Configure proper CORS origins
- [ ] Use strong passwords for database
- [ ] Enable database backups
- [ ] Monitor JWT token expiration
- [ ] Implement token refresh endpoints
- [ ] Use environment variables for secrets
- [ ] Log authentication attempts
- [ ] Implement rate limiting
- [ ] Use secure cookie settings (if needed)

### Best Practices

1. **Secret Keys**
   - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Minimum 32 characters
   - Different keys for JWT and session
   - Rotate periodically

2. **Token Management**
   - Keep tokens short-lived (24 hours recommended)
   - Implement refresh token endpoint
   - Revoke tokens on logout
   - Store expiration in database

3. **Database Security**
   - Use strong passwords
   - Limit database access to app server only
   - Enable SSL for database connections
   - Regular backups and testing

4. **API Security**
   - Validate all inputs
   - Use HTTPS only
   - Implement rate limiting
   - Log security events
   - Monitor for suspicious activity

## Troubleshooting

### JWT Token Not Working

**Issue:** "Invalid token" errors
- Check JWT_SECRET_KEY matches between login and protected endpoint
- Verify token hasn't expired
- Check Authorization header format: `Bearer <token>`

### Database Connection Failed

**Issue:** "Can't connect to MySQL server"
- Verify MYSQL_HOST is correct (use "db" for Docker, "localhost" for local)
- Check MYSQL_PORT is open
- Verify database credentials
- Ensure MySQL service is running

### Token Not in Database

**Issue:** User from token not found in database
- Verify user was created before login
- Check UID format matches (should be UUID)
- Verify token wasn't generated by different app instance
- Check database transaction was committed

## Configuration Changes Checklist

When modifying configuration:

```
[ ] Update .env file
[ ] Restart Flask application
[ ] Verify config with: flask shell > app.config
[ ] Test login endpoint
[ ] Test protected endpoint
[ ] Verify database connectivity
[ ] Check JWT token generation
[ ] Run integration tests
[ ] Monitor application logs
```

## References

- **Flask-JWT-Extended**: https://flask-jwt-extended.readthedocs.io/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/
- **JWT Tokens**: https://tools.ietf.org/html/rfc7519
- **OWASP Security**: https://owasp.org/www-project-top-ten/
