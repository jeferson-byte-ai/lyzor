from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.conversations import Conversation
import uuid

async def create_conversation(db: AsyncSession, org_id: uuid.UUID, title: str | None = None) -> Conversation:
    conv = Conversation(org_id=org_id, title=title)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv

async def get_conversation(db: AsyncSession, conv_id: uuid.UUID) -> Conversation | None:
    return await db.get(Conversation, conv_id)

async def delete_conversation(db: AsyncSession, conv_id: uuid.UUID) -> None:
    await db.execute(delete(Conversation).where(Conversation.id == conv_id))
    await db.commit()
