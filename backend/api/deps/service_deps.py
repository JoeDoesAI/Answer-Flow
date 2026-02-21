from services.file_service.file_uploader import FileUploader
from api.deps.db_deps import get_db,get_qdrant
from api.deps.uploader_deps import get_supabase
from fastapi import Depends

from services.file_service.file_parser import FileParser
from services.embedding_service.embedding import EmbeddingService
from services.ingestion_service.store_vectors import VectorDB
from services.ingestion_service.ochestrator import IngestionOchestrator


async def get_uploader(db = Depends(get_db),supabase=Depends(get_supabase)) -> FileUploader:
    return FileUploader(db,supabase)


async def get_ingestion() -> IngestionOchestrator:
    parser = FileParser()
    embedder = EmbeddingService()
    vector_store = VectorDB(Depends(get_qdrant))
    
    return IngestionOchestrator(parser,embedder,vector_store)

async def get_retrival():
    pass

async def ai_service():
    pass