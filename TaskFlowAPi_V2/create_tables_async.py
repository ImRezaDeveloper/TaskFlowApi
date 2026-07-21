# create_tables.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.taskflow.core.config import DATABASE_URL
from src.taskflow.models import Base

async def main():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())