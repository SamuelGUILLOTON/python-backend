#lib import
from cryptography.fernet import Fernet

f = Fernet('WTq9t7cYyqYlSUpfWzftN97bg0X0lGMIGTYUzZJQIRA=')

#fonctions pour encrypter et décrypter des donner en utlisant fernet
def encrypt(value: str):
    return f.encrypt(value.encode()) 

def decrypt(value: str):
    return f.decrypt(value).decode()