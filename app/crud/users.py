from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.db.models.users import User
import uuid

# =========================
# CRUD Básico de Usuário
# =========================
async def create_user(db: AsyncSession, email: str, username: str, password_hash: str) -> User:
    user = User(email=email, username=username, password_hash=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await db.get(User, user_id)

async def update_user(db: AsyncSession, user_id: uuid.UUID, **kwargs) -> User | None:
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
    password_hash: str | None = None,
    google_id: str | None = None,
    microsoft_id: str | None = None,
    phone_number: str | None = None,
    phone_verified: bool = False,
) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        google_id=google_id,
        microsoft_id=microsoft_id,
        phone_number=phone_number,
        phone_verified=phone_verified
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_google(db: AsyncSession, google_id: str) -> User | None:
    result = await db.execute(select(User).where(User.google_id == google_id))
    return result.scalars().first()

async def get_user_by_microsoft(db: AsyncSession, microsoft_id: str) -> User | None:
    result = await db.execute(select(User).where(User.microsoft_id == microsoft_id))
    return result.scalars().first()

async def get_user_by_phone(db: AsyncSession, phone_number: str) -> User | None:
    result = await db.execute(select(User).where(User.phone_number == phone_number))
    return result.scalars().first()
