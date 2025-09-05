from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.integrations import Integration
import uuid

async def create_integration(db: AsyncSession, org_id: uuid.UUID, provider: str, config: dict) -> Integration:
    integration = Integration(org_id=org_id, provider=provider, config=config)
    db.add(integration)
    await db.commit()
    await db.refresh(integration)
    return integration

async def get_integrations(db: AsyncSession, org_id: uuid.UUID):
    result = await db.execute(select(Integration).where(Integration.org_id == org_id))
    return result.scalars().all()

async def delete_integration(db: AsyncSession, integration_id: uuid.UUID) -> None:
    await db.execute(delete(Integration).where(Integration.id == integration_id))
    await db.commit()
