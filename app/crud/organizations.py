from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.db.models.organizations import Organization, OrganizationMember
import uuid

async def create_org(db: AsyncSession, name: str) -> Organization:
    org = Organization(name=name)
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org

async def add_member(db: AsyncSession, org_id: uuid.UUID, user_id: uuid.UUID, role: str = "member") -> OrganizationMember:
    member = OrganizationMember(org_id=org_id, user_id=user_id, role=role)
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member

async def remove_member(db: AsyncSession, member_id: uuid.UUID) -> None:
    await db.execute(delete(OrganizationMember).where(OrganizationMember.id == member_id))
    await db.commit()
