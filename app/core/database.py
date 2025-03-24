from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Create Async Session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get DB Session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
