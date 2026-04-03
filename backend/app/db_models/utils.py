"""Database model utility functions."""

from app.db_models import User
from sqlalchemy import text


def _getUserRoleByEmail(email: str) -> str:
    """Get user role by email address.
    
    Args:
        email (str): User's email address
        
    Returns:
        str: User's role (DONOR, NGO, ADMIN, DELIVERY_PARTNER)  or None if not found
    """
    if not email:
        return None
    
    try:
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            return user.role
        return None
    except Exception:
        return None


def _getUserRoleByUsername(username: str) -> str:
    """Get user role by username/name.
    
    Note: Since the User model doesn't have a username field,
    this uses the name field for lookups.
    
    Args:
        username (str): User's name
        
    Returns:
        str: User's role (DONOR, NGO, ADMIN, DELIVERY_PARTNER) or None if not found
    """
    if not username:
        return None
    
    try:
        user = User.query.filter(
            User.name.ilike(f"%{username}%")
        ).first()
        if user:
            return user.role
        return None
    except Exception:
        return None
