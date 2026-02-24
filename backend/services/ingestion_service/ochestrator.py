import asyncio
from typing import List

from services.file_service.file_parser import FileParser
from services.embedding_service.embedding import EmbeddingService
from services.ingestion_service.store_vectors import VectorDB


class IngestionOchestrator:
    def __init__(self,file_parser:FileParser, embedder:EmbeddingService, vector_store:VectorDB):
        # Store instances of your sub-pipeline classes
        self.parse_file = file_parser
        self.embedded_text = embedder
        self.vector_store = vector_store

    async def run(self) -> List[dict]:
        doc_text = await self.parse_file.run()
        
        embeddings = self.embedded_text.run(doc_text)

        for doc in doc_text:
            await self.vector_store.store_vectors(embeddings,doc)

        return "Ingestion complete!"



