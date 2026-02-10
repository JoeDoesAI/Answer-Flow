import uuid
import shutil
import asyncio
from typing import List
from pathlib import Path

from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile,HTTPException

from models.sqlite.file_name_store import FileNameStore


class SaveFile:
    """
    save file is a class that validates and saves file to the upload folder of my app
    input a list of file objects into the run method and 

    it validates = a validators work 
        input - UploadFile
        output - List[dict] {valid,errors}

    changes the filename and stores it = create a unique file name
        input - UploadFile, db + model
        output - none

    
    saves the file to the upload folder 
        input - file 
        output - none
    """

    def __init__(self, max_files: int=10,
                       max_size:int = 20 * 1024 * 1024,
                       allowed_extensions:List = [".pdf",".txt",".json"],
                       upload_path:Path = Path("uploads")
                       ):
        
        self.max_size = max_size
        self.max_files = max_files
        self.allowed_extensions = allowed_extensions
        self.upload_path = upload_path


    async def run(self, files: List[UploadFile],db:AsyncSession) -> List[dict]:
        if len(files) > self.max_files:
            return HTTPException (status_code=400,
                detail="Too many files. Maximum 10 files allowed.")
        
        upload_state:List[dict] = []

        for file in files:
            validate_file = await self.validate_file(file)

            file_ext = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path:Path = self.upload_path / unique_filename
            filename:str = file.filename

            if not validate_file["valid"]:
                upload_state.append({
                    "filename": file.filename,
                    "success": False,
                    "errors": validate_file["errors"]
                })
                
                continue

            
    
            upload_file = await self.upload_file(file,file_path)

            if not upload_file["uploaded"]:
                upload_state.append(
                    {"filename": filename,
                    "success": False,
                    "error": upload_file["error"]}
                    )
                
                continue
            


            await self.save_file_name(db,filename,unique_filename)

            upload_state.append({"filename":file.filename,
                                "success":True,
                                })
            
        return upload_state

        
    async def validate_file(self, file:UploadFile) -> dict:
        result = {"valid": True, "errors":[]}

        if not file.filename or not file.filename.strip():
            result["valid"] = False
            result["error"].append("no file selected")

            return result

        #check file extension
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in self.allowed_extensions:
            result["valid"] = False
            result["error"].append(f"The file extension {file_ext} not allowed")

            return result

        #check file size
        content_size = await file.read()
        await file.seek(0)

        file_size = len(content_size)

        if file_size > self.max_size:
            result["valid"] = False
            result["error"].append(
            f"File too large ({file_size:,} bytes). Maximum: {self.max_size:,} bytes"
            )

        return result
    
    async def save_file_name(self,db:AsyncSession,filename:str, unique_filename:str):
        current_date = date.today()
        current_time = datetime.now()


        new_file = FileNameStore(date=current_date,
                                time=current_time,
                                stored_file_name = unique_filename,
                                original_file_name = filename)
        db.add(new_file)

        await db.commit()
        # await db.refresh()


    async def upload_file(self, file:UploadFile, file_path:Path) -> dict:
        upload_state = {}

        try:
            file.file.seek(0)


            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            upload_state["uploaded"] = True

        except Exception as e:
            upload_state["uploaded"] = False
            upload_state["error"] = f"File was not uploaded {e}"

        finally:
            file.file.close()


        return upload_state


        

        

        
        

    

