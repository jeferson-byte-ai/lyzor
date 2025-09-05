from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.sessions import Session
import uuid
from datetime import datetime

async def create_session(db: AsyncSession, user_id: uuid.UUID, token: str, expires_at: datetime) -> Session:
    session = Session(user_id=user_id, token=token, expires_at=expires_at)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def get_session(db: AsyncSession, session_id: uuid.UUID) -> Session | None:
    return await db.get(Session, session_id)

async def delete_session(db: AsyncSession, session_id: uuid.UUID) -> None:
    await db.execute(delete(Session).where(Session.id == session_id))
    await db.commit()

async def delete_expired_sessions(db: AsyncSession) -> None:
    await db.execute(delete(Session).where(Session.expires_at < datetime.utcnow()))
    await db.commit()
