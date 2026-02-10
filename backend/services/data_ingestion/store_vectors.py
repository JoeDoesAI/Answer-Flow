import os
from typing import List

from dotenv import load_dotenv

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")


class VectorDB:
    def __init__(
        self,
        qdrant_url: str = QDRANT_URL,
        collection_name: str = "company_knowledge_base",
    ):
        self.client = AsyncQdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        # Collection creation is async; ensure it when storing vectors

    async def _ensure_collection(self):
        try:
            await self.client.get_collection(self.collection_name)
        except Exception:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=4, distance=Distance.DOT),
            )

    async def store_vectors(self, id: int, vectors: List, payload: dict):
        point = PointStruct(id=id, vector=vectors, payload=payload)

        # points.append(point)
        await self._ensure_collection()

        await self.client.upsert(
            collection_name=self.collection_name, points=[point], wait=True
        )

    async def search_vectors(self, vectors,limit:int=5):
        search_result = await self.client.search(
                collection_name = self.collection_name,
                query_vector=vectors,
                limit=limit,

        )

        payloads = [hit.payload for hit in search_result]

        return {"results":payloads}


