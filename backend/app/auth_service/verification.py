from app.auth_service.hashing import checkPasswordHash
from app.db_models import User

def __getPasswordHashByEmail__(email: str) -> str:
    """Fetch password hash by email (case-insensitive).
    
    BUG FIX #3: Added defensive NULL handling
    BUG FIX #2: Added .lower() for case-insensitive email lookup
    """
    if not email:
        return ""
    
    user = User.query.filter_by(email=email.lower()).first()
    # Defensive: Check for both None and empty/null password_hash
    if not user or not user.password_hash:
        return ""
    return user.password_hash

def __getPasswordHashByUsername__(username: str) -> str:
    """Fetch password hash by username (case-insensitive).
    
    Note: Since the User model doesn't have a username field,
    this uses the name field for lookups.
    """
    if not username:
        return ""
    
    # Try matching by name (case-insensitive)
    user = User.query.filter(
        User.name.ilike(f"%{username}%")
    ).first()
    
    if not user or not user.password_hash:
        return ""
    return user.password_hash

# Login Authentication Service
def verifyEmail(email: str) -> bool:
    """Fetch user by email and verify existence (case-insensitive).
    
    BUG FIX #2: Added .lower() for case-insensitive email lookup
    """
    if not email:
        return False
    user = User.query.filter_by(email=email.lower()).first()
    return user is not None

def verifyUser(username: str) -> bool:
    """Fetch user by name and verify existence (case-insensitive).
    
    Note: Since the User model doesn't have a username field,
    this checks against the name field.
    """
    if not username:
        return False
    user = User.query.filter(
        User.name.ilike(f"%{username}%")
    ).first()
    return user is not None

def verifyPasswordByEmail(email: str, password: str) -> bool:
    """Fetch password hash by email and verify password (case-insensitive).
    
    BUG FIX #2: Added .lower() for case-insensitive email lookup
    """
    if not email or not password:
        return False
    
    _password_hash_ = __getPasswordHashByEmail__(email)
    if _password_hash_ == "":
        return False
    
    return checkPasswordHash(password, _password_hash_)

def verifyPasswordByUsername(username: str, password: str) -> bool:
    """Fetch password hash by username and verify password.
    
    Note: Since the User model doesn't have a username field,
    this uses the name field for lookups.
    """
    if not username or not password:
        return False
    
    _password_hash_ = __getPasswordHashByUsername__(username)
    if _password_hash_ == "":
        return False
    
    return checkPasswordHash(password, _password_hash_)
