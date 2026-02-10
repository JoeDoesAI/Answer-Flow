import asyncio
from typing import List

from fastapi import UploadFile,HTTPException
from db.sqlite.session import AsyncSession


from services.data_ingestion.document_uploader import SaveFile
from services.data_ingestion.file_parser import FileParser
from services.data_ingestion.embedding import EmbeddingService
from services.data_ingestion.store_vectors import VectorStore


class IngestionOchestrator:
    def __init__(self, file_saver:SaveFile, file_parser:FileParser, embedder:EmbeddingService, vector_store:VectorStore):

        # Store instances of your sub-pipeline classes
        self.save_file = file_saver
        self.parse_file = file_parser
        self.embedded_text = embedder
        self.vector_store = vector_store

    async def run(self, files:List[UploadFile], db:AsyncSession,) -> List[dict]:
        
        await self.save_file.run(files,db)

        doc_text = await self.parse_file.run()
        
        embeddings = await self.embedded_text.run(doc_text)
        
        await self.vector_store.run(embeddings,doc_text)

        return "Ingestion complete!"



