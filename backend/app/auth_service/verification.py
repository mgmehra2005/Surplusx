from app.auth_service.hashing import checkPasswordHash
from app.db_models import User

def __getPasswordHash__(username: str) -> str:
    """Fetch password hash by username."""
    try:
        user = User.query.filter_by(username=username).first()
        return user.hashed_password if user else ""
    except Exception as e:
        print(f"Error fetching password hash for username {username}: {e}")
        return ""


def __getPasswordHashByEmail__(email: str) -> str:
    """Fetch password hash by email."""
    try:
        user = User.query.filter_by(email=email).first()
        return user.hashed_password if user else ""
    except Exception as e:
        print(f"Error fetching password hash for email {email}: {e}")
        return ""

# Login Authentication Service
def verifyUser(username: str) -> bool:
    """Fetch user by username and verify existence."""
    try:
        user = User.query.filter_by(username=username).first()
        return user is not None
    except Exception as e:
        print(f"Error verifying user by username {username}: {e}")
        return False

def verifyEmail(email: str) -> bool:
    """Fetch user by email and verify existence."""
    try:
        user = User.query.filter_by(email=email).first()
        return user is not None
    except Exception as e:
        print(f"Error verifying user by email {email}: {e}")
        return False

def verifyPasswordByUsername(username: str, password: str) -> bool:
    """Fetch password hash by username and verify password."""
    if not username or not password:
        return False
    
    _password_hash_ = __getPasswordHash__(username)
    if _password_hash_ == "":
        return False
    
    return checkPasswordHash(password, _password_hash_)

def verifyPasswordByEmail(email: str, password: str) -> bool:
    """Fetch password hash by email and verify password."""
    if not email or not password:
        return False
    
    _password_hash_ = __getPasswordHashByEmail__(email)
    if _password_hash_ == "":
        return False
    
    return checkPasswordHash(password, _password_hash_)
