import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from app.db.base import Base
import uuid

class Integration(Base):
    __tablename__ = "integrations"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"))
    provider = sa.Column(sa.Text, nullable=False)
    config = sa.Column(JSONB, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
