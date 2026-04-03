from .verification import verifyUser, verifyEmail, verifyPasswordByUsername, verifyPasswordByEmail
import jwt, datetime


def loginWithUsername(user: str, password: str) -> bool:
    print("username", verifyUser(user), "\npassword", verifyPasswordByUsername(user, password))
    if verifyUser(user) and verifyPasswordByUsername(user, password):
        return True
    return False

def loginWithEmail(email: str, password: str) -> bool:
    if verifyEmail(email) and verifyPasswordByEmail(email, password):
        return True
    return False
