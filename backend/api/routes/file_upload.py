from typing import List

from fastapi import APIRouter, Request, File, UploadFile, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.data_ingestion.ochestrator import IngestionOrchestrator

from api.deps import get_db
from api.deps import ingest_docs


uploader_router = APIRouter()



@uploader_router.post("/upload-docs")
async def upload_docs(request: Request, 
                       file:List[UploadFile] = File(),
                       db: AsyncSession = Depends(get_db),
                       ingestor:IngestionOrchestrator = Depends(ingest_docs)
                       ):
    if not request.session.get("authorized"):
        return HTTPException(status_code=400, detail="No Access")

    ingest_files = await ingest_docs(file, db, ingestor)

    if not ingest_files:
        return HTTPException(status_code=404)
    