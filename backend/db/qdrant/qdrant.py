from qdrant_client import AsyncQdrantClient
from app.core.config import settings

class QdrantManager:
    def __init__(self):
        self.client: AsyncQdrantClient = None

    async def connect(self):
        # Using gRPC (port 6334) is recommended for better performance in 2026
        self.client = AsyncQdrantClient(
            url=settings.QDRANT_URL, 
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True 
        )

    async def disconnect(self):
        if self.client:
            await self.client.close()

qdrant_manager = QdrantManager()
