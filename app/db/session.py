from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://lyzor_user:lyzor_pass@localhost:5432/lyzor_db")

# Engine async
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# Session maker async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency para FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
