from typing import AsyncGenerator
from db.sqlite.session import AsyncSession, AsyncSessionLocal
from qdrant_client import AsyncQdrantClient


from services.data_ingestion.document_uploader import SaveFile
from services.data_ingestion.file_parser import FileParser
from services.data_ingestion.embedding import EmbeddingService
from services.data_ingestion.store_vectors import VectorStore
from services.data_ingestion.ochestrator import IngestionOchestrator


# Dependency to get an async session for use in FastAPI route functions
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as session:
            yield session

    finally:
        await session.close()


async def get_file_ingestion() -> IngestionOchestrator:
    uploader = SaveFile()
    parser = FileParser()
    embedder = EmbeddingService()
    vector_store = VectorStore()

    return IngestionOchestrator(uploader,parser,embedder,vector_store)

async def get_answer() -> GenerationOchestrator:
    pass

async def get_qdrant_client() -> AsyncQdrantClient:
    client = AsyncQdrantClient(url=QDRANT_URL)

    return client
# app.state.qdrant_client = AsyncQdrantClient(host="localhost", port=6333)