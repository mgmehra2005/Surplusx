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

# Login Authentication Service
def verifyEmail(email: str) -> bool:
    """Fetch user by email and verify existence (case-insensitive).
    
    BUG FIX #2: Added .lower() for case-insensitive email lookup
    """
    if not email:
        return False
    user = User.query.filter_by(email=email.lower()).first()
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
