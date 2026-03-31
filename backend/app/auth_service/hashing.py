from werkzeug.security import generate_password_hash, check_password_hash

def hashPassword(password: str) -> str:
    """Hash a plaintext password."""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def checkPasswordHash(password: str, hashed_password: str) -> bool:
    """Check if a plaintext password matches a hashed password."""
    return check_password_hash(hashed_password, hashPassword(password))