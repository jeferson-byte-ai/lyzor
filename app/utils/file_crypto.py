from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("FERNET_KEY", Fernet.generate_key().decode())
fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

def encrypt_file(input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(output_path, "wb") as f:
        f.write(encrypted)

def decrypt_file(input_path: str, output_path: str):
    with open(input_path, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    with open(output_path, "wb") as f:
        f.write(decrypted)
