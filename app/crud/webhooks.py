from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.webhooks import Webhook, WebhookDelivery
import uuid

async def create_webhook(db: AsyncSession, org_id: uuid.UUID, url: str, secret: str) -> Webhook:
    webhook = Webhook(org_id=org_id, url=url, secret=secret)
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    return webhook

async def get_webhooks(db: AsyncSession, org_id: uuid.UUID):
    result = await db.execute(select(Webhook).where(Webhook.org_id == org_id))
    return result.scalars().all()

async def delete_webhook(db: AsyncSession, webhook_id: uuid.UUID) -> None:
    await db.execute(delete(Webhook).where(Webhook.id == webhook_id))
    await db.commit()

async def create_webhook_delivery(db: AsyncSession, webhook_id: uuid.UUID, payload: dict, success: bool = False) -> WebhookDelivery:
    delivery = WebhookDelivery(webhook_id=webhook_id, payload=payload, success=success)
    db.add(delivery)
    await db.commit()
    await db.refresh(delivery)
    return delivery

async def get_webhook_deliveries(db: AsyncSession, webhook_id: uuid.UUID, limit: int = 50):
    result = await db.execute(
        select(WebhookDelivery)
        .where(WebhookDelivery.webhook_id == webhook_id)
        .order_by(WebhookDelivery.delivered_at.desc())
        .limit(limit)
    )
    return result.scalars().all()
