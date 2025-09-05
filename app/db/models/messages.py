import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"

    id = sa.Column(sa.BigInteger, primary_key=True)
    conv_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("conversations.id", ondelete="CASCADE"))
    sender_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"))
    content = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
