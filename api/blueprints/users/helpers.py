from re import fullmatch

import bcrypt
from common.models import User

def is_email_correct(email: str) -> bool:
    email_regex = r'[a-z0-9\-.]+@[a-z0-9\-.]+\.[a-z]{2,4}'
    return fullmatch(email_regex, email)

def is_email_registered(email: str) -> bool:
    return User.query.filter_by(email=email).first() is not None

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(user: User, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), user.password.encode())
