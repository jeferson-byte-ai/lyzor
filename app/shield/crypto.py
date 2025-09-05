from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY must be set")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(plain_text: str) -> str:
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    return fernet.decrypt(encrypted_text.encode()).decode()
