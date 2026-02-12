from typing import List
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams


class VectorDB:
    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str = "company_knowledge_base",
    ):
        self.client = client
        self.collection_name = collection_name
        

    async def store_vectors(self, id: int, vectors: List, payload: dict):
        point = PointStruct(id=id, vector=vectors, payload=payload)

        await self.client.upsert(
            collection_name=self.collection_name, points=[point], wait=True
        )

    async def search_vectors(self, vectors,limit:int=5):
        await self._ensure_collection()

        search_result = await self.client.search(
                collection_name = self.collection_name,
                query_vector=vectors,
                limit=limit,

        )

        payloads = [hit.payload for hit in search_result]

        return {"results":payloads}


