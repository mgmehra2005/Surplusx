from .verification import verifyUser, verifyEmail
from app.db_models import User
from .hashing import hashPassword
from app import db


def registerUser(username: str, email: str, password: str, user_role:str, phone_number:str, fullName: str) -> bool:
    if verifyUser(username) or verifyEmail(email):
        return False  # User already exists
    
    try:
        hashed_password = hashPassword(password)
        # Create and save the new user
        new_user = User(
            name = fullName,
            username=username, 
            email=email,
            password_hash=hashed_password,
            role="DONOR"  if not user_role else user_role,  # Default role DONOR
            phone= "NULL" if not phone_number else phone_number
        )
        db.session.add(new_user)
        db.session.commit()
        return True
    
    except Exception as e:
        print(f"Error occurred while registering user: {e}")
        return False