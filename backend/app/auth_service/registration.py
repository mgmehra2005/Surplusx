from .verification import verifyEmail
from app.db_models import User
from .hashing import hashPassword
from app import db
from app.utils import normalize_email, validate_email_format, sanitize_input, validate_password_strength
import uuid
import logging

logger = logging.getLogger(__name__)

def registerUser(email: str, name: str, password: str, role: str = 'DONOR') -> dict:
    """Register a new user in the database.
    
    BUG FIX #1: Implemented missing registerUser function
    
    Args:
        email (str): User's email address
        name (str): User's full name
        password (str): User's password (will be hashed)
        role (str): User's role (DONOR, NGO, ADMIN, DELIVERY_PARTNER)
    
    Returns:
        dict: {"success": bool, "message": str, "user": dict or None}
    """
    # Input validation
    if not email or not name or not password:
        return {
            "success": False,
            "message": "Email, name, and password are required",
            "user": None
        }
    
    # Normalize email to lowercase for case-insensitive comparison
    email = normalize_email(email)
    
    # Validate email format
    if not validate_email_format(email):
        return {
            "success": False,
            "message": "Invalid email format",
            "user": None
        }
    
    # Sanitize name
    try:
        name = sanitize_input(name, max_length=100)
    except ValueError:
        return {
            "success": False,
            "message": "Invalid name format",
            "user": None
        }
    
    # Check if user already exists (case-insensitive)
    if verifyEmail(email):
        return {
            "success": False,
            "message": "Email already registered",
            "user": None
        }
    
    # Validate password strength (must have uppercase, lowercase, digit, special char, 8+ chars)
    is_valid, password_message = validate_password_strength(password)
    if not is_valid:
        return {
            "success": False,
            "message": password_message,
            "user": None
        }
    
    # Validate role
    valid_roles = ['DONOR', 'NGO', 'DELIVERY_PARTNER', 'ADMIN']
    if role not in valid_roles:
        return {
            "success": False,
            "message": f"Invalid role. Must be one of: {', '.join(valid_roles)}",
            "user": None
        }
    
    try:
        # Create new user
        new_user = User(
            uid=str(uuid.uuid4()),
            name=name,
            email=email,  # Store email in lowercase (already normalized)
            password_hash=hashPassword(password),
            role=role,
            phone=None
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        return {
            "success": True,
            "message": "User registered successfully",
            "user": {
                "uid": new_user.uid,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            }
        }
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return {
            "success": False,
            "message": "Registration failed. Please try again.",
            "user": None
        }