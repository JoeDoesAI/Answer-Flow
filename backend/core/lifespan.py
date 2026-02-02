from contextlib import asynccontextmanager

from fastapi import FastAPI

import models
from db.sqlite.engine import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
        
   
    await engine.dispose()
