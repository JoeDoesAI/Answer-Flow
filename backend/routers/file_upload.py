import os
import uuid
import shutil
from typing import List
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse,RedirectResponse

from services.document_validator import DocumentValidator


uploader_router = APIRouter()


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


doc_validator = DocumentValidator()

@uploader_router.post("/upload-file")
async def upload_file(request: Request, file:UploadFile = File()):
    if request.session.get("authorized"):
        validation = await doc_validator.validate_file(file)

        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "File validation failed",
                    "errors": validation["errors"]
                }
            )
    
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"File upload failed: {str(e)}")
        
        finally:
            file.file.close()
        
        return {
            "success": True,
            "original_filename": file.filename,
            "stored_filename": unique_filename,
            "content_type": file.content_type,
            "size": file.size,
            "upload_time": datetime.utcnow().isoformat(),
            "location": str(file_path)
        }

    return HTTPException(status_code=400, detail="No Access")


@uploader_router.post("/upload-files")
async def upload_files(request: Request, files:List[UploadFile] = File()):
    if request.session.get("authorized"):
        if len(files) > 10:  # Limit number of files
            raise HTTPException(
                status_code=400,
                detail="Too many files. Maximum 10 files allowed."
            )
        
        results = []

        for file in files:
            validation = await doc_validator.validate_file(file)

            if not validation["valid"]:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "errors": validation["errors"]
                })
                
                continue
            
            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = UPLOAD_DIR / unique_filename


            try:
                file.file.seek(0)


                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                results.append({
                    "filename": file.filename,
                    "stored_filename": unique_filename,
                    "success": True,
                    "location": str(file_path)
                })

            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "errors": [f"Failed to save: {str(e)}"]
                })

            finally:
                file.file.close()

        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        return {
            "total_files": len(files),
            "successful": len(successful),
            "failed": len(failed),
            "upload_time": datetime.utcnow().isoformat(),
            "results": results
        }
    
    return HTTPException(status_code=400, detail="No Access")


        