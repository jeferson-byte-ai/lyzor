import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from app.db.base import Base

class Webhook(Base):
    __tablename__ = "webhooks"

    id = sa.Column(UUID(as_uuid=True), primary_key=True)
    org_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"))
    url = sa.Column(sa.Text, nullable=False)
    secret = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    id = sa.Column(sa.BigInteger, primary_key=True)
    webhook_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("webhooks.id", ondelete="CASCADE"))
    payload = sa.Column(JSONB, nullable=False)
    delivered_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
    success = sa.Column(sa.Boolean, default=False)
