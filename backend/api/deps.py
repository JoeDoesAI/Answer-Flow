from db.sqlite.session import AsyncSession, AsyncSessionLocal
from services.data_ingestion.ochestrator import IngestionOrchestrator


# Dependency to get an async session for use in FastAPI route functions
async def get_db() -> AsyncSession:
    try:
        async with AsyncSessionLocal() as session:
            yield session

    finally:
        await session.close()


async def ingest_docs():
    

# async def get_qdrant():
#     return qdrant_client