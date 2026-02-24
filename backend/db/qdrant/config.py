from qdrant_client import AsyncQdrantClient
from core.config import Settings

QDRANT_URL = Settings.QDRANT_URL
QDRATN_API_KEY = Settings.QDRANT_API_KEY



def init_qdrant():
    return AsyncQdrantClient(url=QDRANT_URL,api_key=QDRATN_API_KEY)

async def ensure_collection(qdrant:AsyncQdrantClient):
    if not qdrant.collection_exists("company_knowledge_base"):
        await qdrant.create_collection(
            collection_name="company_knowledge_base",
            vectors_config={
                "size": 384,
                "distance": "Cosine"
            }
        )


