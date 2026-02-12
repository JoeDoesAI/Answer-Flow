from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.sqlite.engine import engine, Base
from db.qdrant.config import init_qdrant,ensure_collection

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    
    qdrant =  init_qdrant()

    await ensure_collection(qdrant)

    app.state.qdrant = qdrant


    yield
        
   #shutdown
    await engine.dispose()
