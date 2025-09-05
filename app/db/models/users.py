import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.Text, unique=True, nullable=True)  # nem todo usuário terá email
    username = sa.Column(sa.Text, unique=True, nullable=False)
    password_hash = sa.Column(sa.Text, nullable=True)  # para OAuth pode ser None

    google_id = sa.Column(sa.Text, unique=True, nullable=True)
    microsoft_id = sa.Column(sa.Text, unique=True, nullable=True)

    phone_number = sa.Column(sa.Text, unique=True, nullable=True)
    phone_verified = sa.Column(sa.Boolean, default=False)

    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        sa.Index("idx_users_email", "email"),
        sa.Index("idx_users_google_id", "google_id"),
        sa.Index("idx_users_microsoft_id", "microsoft_id"),
        sa.Index("idx_users_phone_number", "phone_number"),
    )
