from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.db.models.users import User
import uuid

# Shield
from app.shield.security import hash_password, encrypt_data, decrypt_data

# =========================
# Basic User CRUD
# =========================
async def create_user(db: AsyncSession, email: str, username: str, password: str) -> User:
    password_hash = hash_password(password)
    encrypted_email = encrypt_data(email)
    user = User(email=encrypted_email, username=username, password_hash=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    user = await db.get(User, user_id)
    if user and user.email:
        user.email = decrypt_data(user.email)
    return user

async def update_user(db: AsyncSession, user_id: uuid.UUID, **kwargs) -> User | None:
    # encrypt email if updated
    if 'email' in kwargs and kwargs['email']:
        kwargs['email'] = encrypt_data(kwargs['email'])
    await db.execute(update(User).where(User.id == user_id).values(**kwargs))
    await db.commit()
    return await get_user(db, user_id)

async def delete_user(db: AsyncSession, user_id: uuid.UUID) -> None:
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

# =========================
# OAuth2 / Phone Login CRUD
# =========================
async def create_user_oauth(
    db: AsyncSession,
    username: str,
    email: str | None = None,
    password: str | None = None,
    google_id: str | None = None,
    microsoft_id: str | None = None,
    phone_number: str | None = None,
    phone_verified: bool = False,
) -> User:
    password_hash = hash_password(password) if password else None
    encrypted_email = encrypt_data(email) if email else None
    encrypted_phone = encrypt_data(phone_number) if phone_number else None

    user = User(
        username=username,
        email=encrypted_email,
        password_hash=password_hash,
        google_id=google_id,
        microsoft_id=microsoft_id,
        phone_number=encrypted_phone,
        phone_verified=phone_verified
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_google(db: AsyncSession, google_id: str) -> User | None:
    result = await db.execute(select(User).where(User.google_id == google_id))
    user = result.scalars().first()
    if user and user.email:
        user.email = decrypt_data(user.email)
    return user

async def get_user_by_microsoft(db: AsyncSession, microsoft_id: str) -> User | None:
    result = await db.execute(select(User).where(User.microsoft_id == microsoft_id))
    user = result.scalars().first()
    if user and user.email:
        user.email = decrypt_data(user.email)
    return user

async def get_user_by_phone(db: AsyncSession, phone_number: str) -> User | None:
    encrypted_phone = encrypt_data(phone_number)
    result = await db.execute(select(User).where(User.phone_number == encrypted_phone))
    user = result.scalars().first()
    if user and user.phone_number:
        user.phone_number = decrypt_data(user.phone_number)
    return user
