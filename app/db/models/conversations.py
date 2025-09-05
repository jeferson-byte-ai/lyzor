import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base
import uuid

class Conversation(Base):
    __tablename__ = "conversations"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"))
    title = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
