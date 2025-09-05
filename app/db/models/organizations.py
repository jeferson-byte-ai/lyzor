import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.base import Base
import uuid

class Organization(Base):
    __tablename__ = "organizations"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"))
    role = sa.Column(sa.Text, default="member")
    joined_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
