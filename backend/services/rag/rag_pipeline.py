# from typing import List, Any

# from services.parse_files import DocumentParser
# from services.late_chunking import LateChunkEmbed
# from services.store_vectors import VectorStore


# chunker = LateChunkEmbed()
# vector_store = VectorStore()


# class RAGPipeline:
#     def __init__(self, db: Any):
#         self.db = db

#     async def run(self):
#         """Full automated pipeline"""

#         try:
#             parsed_content = await self.parse()

#             for idx, page in enumerate(parsed_content, start=1):
#                 embeddings = await self.embed(page["text"])

#                 payload = {
#                     "source_file": page.get("filename"),
#                     "page_number": page.get("page_number"),
#                     "chunk_text": page.get("text"),
#                 }

#                 await self.store(idx, embeddings, payload)

#         except Exception:
#             raise

#     async def parse(self) -> List[dict]:
#         parser = DocumentParser(self.db)
#         return await parser.parse_doc()

#     async def embed(self, text: str) -> List[List[float]]:
#         return chunker.late_chunk(text)

#     async def store(self, id: int, vectors: List, payload: dict):
#         await vector_store.store_vectors(id, vectors, payload)



# class RAGPipeline:
#     def __init__(self, processor, chunker, embedder, vector_store):
#         # Store instances of your sub-pipeline classes
#         self.processor = processor
#         self.chunker = chunker
#         self.embedder = embedder
#         self.vector_store = vector_store

#     def run_ingestion(self, raw_data):
#         # Link them by passing output from one to the input of the next
#         clean_text = self.processor.process(raw_data)
#         chunks = self.chunker.generate_chunks(clean_text)
#         embeddings = self.embedder.embed(chunks)
#         self.vector_store.save(chunks, embeddings)
#         return "Ingestion complete!"

# # Usage
# pipeline = RAGPipeline(
#     processor=DocProcessor(),
#     chunker=ChunkGenerator(),
#     embedder=EmbeddingService(),
#     vector_store=VectorDB()
# )
# pipeline.run_ingestion("my_file.pdf")
