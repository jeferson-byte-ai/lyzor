from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.messages import Message
import uuid

async def create_message(db: AsyncSession, conv_id: uuid.UUID, sender_id: uuid.UUID | None, content: str) -> Message:
    msg = Message(conv_id=conv_id, sender_id=sender_id, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def get_messages(db: AsyncSession, conv_id: uuid.UUID, limit: int = 50):
    result = await db.execute(
        select(Message).where(Message.conv_id == conv_id).order_by(Message.created_at.desc()).limit(limit)
    )
    return result.scalars().all()

async def delete_message(db: AsyncSession, message_id: int) -> None:
    await db.execute(delete(Message).where(Message.id == message_id))
    await db.commit()
