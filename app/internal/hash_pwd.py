# System imports
import hashlib

def hash_password(password: str) -> str:
    hash_object = hashlib.sha256(password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()
    return hashed_password