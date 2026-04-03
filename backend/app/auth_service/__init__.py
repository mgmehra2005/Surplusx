from .verification import verifyEmail, verifyPasswordByEmail
from .registration import registerUser
from app.db_models import User
from typing import Optional, Dict, Any

def loginWithEmail(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user by email and return user data if successful.
    
    BUG FIX #2: Uses case-insensitive email lookup
    """
    if not email or not password:
        return None
    
    if verifyEmail(email) and verifyPasswordByEmail(email, password):
        # Use lowercase email for consistent database lookup
        user_obj = User.query.filter_by(email=email.lower()).first()
        if user_obj:
            return {
                'uid': user_obj.uid,
                'name': user_obj.name,
                'email': user_obj.email,
                'role': user_obj.role
            }
    return None


# Export functions for external use
__all__ = ['loginWithEmail', 'registerUser']