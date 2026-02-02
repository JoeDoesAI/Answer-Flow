import uuid
from datetime import datetime, date
import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile,HTTPException

UPLOAD_DIR = Path("uploads").parent.parent
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class SaveFile:
    def __init__(self, max_files: int=10,
                       max_size:int = 20 * 1024 * 1024,
                       allowed_extensions:List = [".pdf",".txt",".json"],
                       upload_path = Path("uploads").parent.parent
                       ):
        self.max_size = max_size
        self.max_files = max_files
        self.allowed_extensions = allowed_extensions
        self.upload_path = upload_path

    async def run(self, files: List[UploadFile]):
        if len(files) > self.max_files:
            return HTTPException (status_code=400,
                detail="Too many files. Maximum 10 files allowed.")
        
        upload_state = []

        for file in files:
            validate_file = await self.validate_file(file)

            if not validate_file["valid"]:
                upload_state.append({
                    "filename": file.filename,
                    "success": False,
                    "errors": validate_file["errors"]
                })
                
                continue

            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = self.upload_path / unique_filename




            

        
    async def validate_file(self, file:UploadFile) -> dict:
        result = {"valid": True, "errors":[]}

        if not file.filename or not file.filename.strip():
            result["valid"] = False
            result["errors"].append("no file selected")

            return result

        #check file extension
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in self.allowed_extensions:
            result["valid"] = False
            result["errors"].append(f"The file extension {file_ext} not allowed")

            return result

        #check file size
        content_size = await file.read()
        await file.seek(0)

        file_size = len(content_size)

        if file_size > self.max_size:
            result["valid"] = False
            result["errors"].append(
            f"File too large ({file_size:,} bytes). Maximum: {self.max_size:,} bytes"
            )

        return result

            
    async def upload_file(self, file:UploadFile):
        try:
            file.file.seek(0)


            with open(self.upload_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            current_date = date.today()
            current_time = datetime.now()

            new_file = FileNameStore(date=current_date,
                                    time=current_time,
                                    stored_file_name = unique_filename,
                                    original_file_name = file.filename)
            db.add(new_file)

            await db.commit()
            await db.refresh()


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

    # process_docs = RAGPipeline(db)
    # await process_docs.run()

    return {
        "total_files": len(files),
        "successful": len(successful),
        "failed": len(failed),
        "upload_time": datetime.utcnow().isoformat(),
        "results": results
    }
    
    return HTTPException(status_code=400, detail="No Access")


        

        
        

    

