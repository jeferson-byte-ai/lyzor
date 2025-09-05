import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base
import uuid

class Session(Base):
    __tablename__ = "sessions"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"))
    token = sa.Column(sa.Text, unique=True, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
    expires_at = sa.Column(sa.DateTime(timezone=True), nullable=False)
