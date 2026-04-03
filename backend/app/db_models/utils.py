from app.db_models import User

def _getUserRoleByUsername(username: str) -> str:
    """Fetch user role by username."""
    try:
        user = User.query.filter_by(username=username).first()
        return user.role if user else ""
    except Exception as e:
        print(f"Error fetching user role for username {username}: {e}")
        return ""
    
def _getUserRoleByEmail(email: str) -> str:
    """Fetch user role by email."""
    try:
        user = User.query.filter_by(email=email).first()
        return user.role if user else ""
    except Exception as e:
        print(f"Error fetching user role for email {email}: {e}")
        return ""