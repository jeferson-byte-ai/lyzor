from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.users import User
from app.shield.security import hash_password, encrypt_data, decrypt_data, verify_password
from sqlalchemy import select, update, delete
import uuid

# ----------------------
# Create user with email/password
# ----------------------
async def create_user(db: AsyncSession, username: str, email: str, password: str):
    user = User(
        username=username,
        email=encrypt_data(email),
        password_hash=hash_password(password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# ----------------------
# CRUD read
# ----------------------
async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID):
    return await db.get(User, user_id)

async def get_user_email(user: User):
    return decrypt_data(user.email)

async def verify_user_password(user: User, password: str):
    return verify_password(password, user.password_hash)

# ----------------------
# OAuth2 / Phone Login CRUD
# ----------------------
async def create_user_oauth(
    db: AsyncSession,
    username: str,
    email: str | None = None,
    password_hash: str | None = None,
    google_id: str | None = None,
    microsoft_id: str | None = None,
    phone_number: str | None = None,
    phone_verified: bool = False
) -> User:
    user = User(
        username=username,
        email=encrypt_data(email) if email else None,
        password_hash=password_hash,
        google_id=encrypt_data(google_id) if google_id else None,
        microsoft_id=encrypt_data(microsoft_id) if microsoft_id else None,
        phone_number=encrypt_data(phone_number) if phone_number else None,
        phone_verified=phone_verified
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_google(db: AsyncSession, google_id: str) -> User | None:
    enc_id = encrypt_data(google_id)
    result = await db.execute(select(User).where(User.google_id == enc_id))
    return result.scalars().first()

async def get_user_by_microsoft(db: AsyncSession, microsoft_id: str) -> User | None:
    enc_id = encrypt_data(microsoft_id)
    result = await db.execute(select(User).where(User.microsoft_id == enc_id))
    return result.scalars().first()

async def get_user_by_phone(db: AsyncSession, phone_number: str) -> User | None:
    enc_number = encrypt_data(phone_number)
    result = await db.execute(select(User).where(User.phone_number == enc_number))
    return result.scalars().first()
