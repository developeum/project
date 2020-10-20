from re import fullmatch

def check_email(email: str) -> bool:
    email_regex = r'[a-z0-9\-.]+@[a-z0-9\-.]+\.[a-z]{2,4}'
    return fullmatch(email_regex, email)
