from typing import Annotated
from fastapi import Depends

from services.file_service.file_uploader import FileUploader
from api.deps.db_deps import get_db,get_qdrant
from api.deps.uploader_deps import get_supabase


from services.file_service.file_parser import FileParser
from services.embedding_service.embedding import EmbeddingService
from services.ingestion_service.store_vectors import VectorDB
from services.ingestion_service.ochestrator import IngestionOchestrator

# SupabaseDep = Annotated[AsyncClient, Depends(get_supabase)]

async def get_uploader(db = Depends(get_db),supabase=Depends(get_supabase)) -> FileUploader:
    return FileUploader(db,supabase)


async def get_ingestion(
    supabase_client = Depends(get_supabase),
    db = Depends(get_db),
    qdrant=Depends(get_qdrant)
) -> IngestionOchestrator:
    
   
    parser = FileParser(supabase_client=supabase_client, db=db)
    embedder = EmbeddingService()
    vector_store = VectorDB(qdrant)
    
    return IngestionOchestrator(parser, embedder, vector_store)

async def get_retrival():
    pass

async def ai_service():
    pass