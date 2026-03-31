from .verification import verifyUser, verifyEmail, verifyPasswordByUsername, verifyPasswordByEmail

def loginWithUsername(user: str, password: str) -> bool:
    if verifyUser(user) and verifyPasswordByUsername(user, password):
        return True
    return False

def loginWithEmail(email: str, password: str) -> bool:
    if verifyEmail(email) and verifyPasswordByEmail(email, password):
        return True
    return False


# Register a new user