# app/shield/security.py
import os
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet

# ----------------------
# Password hashing
# ----------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(password, hashed)

# Alias antigo para compatibilidade
get_password_hash = hash_password

# ----------------------
# JWT Authentication
# ----------------------
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_days: int = REFRESH_TOKEN_EXPIRE_DAYS):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# ----------------------
# AES-256 Encryption for sensitive data
# ----------------------
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise RuntimeError("Missing FERNET_KEY in environment variables!")

fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

def encrypt_data(plain_text: str) -> str:
    """Encrypt a string using Fernet"""
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    """Decrypt a string using Fernet"""
    return fernet.decrypt(encrypted_text.encode()).decode()

# =======================
# JWT Token Blacklist
# =======================
jwt_blacklist = set()

def add_token_to_blacklist(token: str):
    jwt_blacklist.add(token)

def is_token_blacklisted(token: str) -> bool:
    return token in jwt_blacklist

def decode_access_token(token: str) -> dict:
    if is_token_blacklisted(token):
        raise Exception("Token has been revoked.")
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
