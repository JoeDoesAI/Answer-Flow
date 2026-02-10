from typing import List

from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Depends
from db.sqlite.session import AsyncSession




from api.deps import get_async_db_session,get_file_ingestion
from services.data_ingestion.ochestrator import IngestionOchestrator

uploader_router = APIRouter()


@uploader_router.post("/upload-docs",response_model=None)
async def upload_docs(
    request: Request,
    db: AsyncSession = Depends(get_async_db_session),
    files: List[UploadFile] = File(...),
    ingestion: IngestionOchestrator = Depends(get_file_ingestion)
):
    if not request.session.get("authorized"):
        raise HTTPException(status_code=400, detail="No Access")

    ingestor = await ingestion.run(files,db)

    return ingestor