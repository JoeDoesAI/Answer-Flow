from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.sqlite.engine import engine, Base
from db.qdrant.config import init_qdrant,ensure_collection
from supabase import create_async_client

from core.config import Settings


SUPABASE_URL = Settings.SUPABASE_URL
SUPABASE_KEY = Settings.SUPABASE_KEY

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    
    qdrant =  init_qdrant()

    await ensure_collection(qdrant)

    app.state.qdrant = qdrant
    app.state.supabase = await create_async_client(SUPABASE_URL, SUPABASE_KEY)
    


    yield
    #shutdown
    
    await app.state.supabase.aclose()
    await engine.dispose()
        
   
   
