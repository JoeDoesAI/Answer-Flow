import io
import os
from pathlib import Path
from typing import List

from docling.datamodel.base_models import DocumentStream
from sqlalchemy import select
from db.sqlite.session import AsyncSession
from docling.document_converter import DocumentConverter
from models.sqlite.file_name_store import FileNameStore
from core.config import Settings
from supabase import AsyncClient




class FileParser:
    def __init__(self,supabase_client:AsyncClient,doc_converter = DocumentConverter(),bucket_name=Settings.SUPABASE_BUCKET, directory_path:Path = Path("uploads")):
        self.converter = doc_converter
        self.bucket = bucket_name
        self.supabase = supabase_client

    async def run(self) -> List[dict]:
        """ Generate a list of dictionaries of each file
        
        dict - filename
               file_content
               page_char_coount
               token_count

        """
        files = self.supabase.storage.from_(self.bucket).list("uploads")

        if not files:
            return "No files in the supabase directory"
        
        markdown_result = []

        for file in files:
            file_name = file["name"]

            if file_name == ".emptyFolderPlaceholder":
                continue

            file_path = f"uploads/{file_name}"
            file_bytes = self.supabase.from_(self.bucket).download(file_path)


            buf = io.BytesIO(file_bytes)
            source = DocumentStream(name=file_name, stream=buf)

            result = self.converter.convert(source)
            markdown_text = result.document.export_to_markdown()




            # converter = self.converter.convert(file_path)
            # markdown_text = converter.document.export_to_markdown()


            doc_data = {
                "filename":file_path,
                "file_content" : markdown_text,
                "page_char_count": len(markdown_text),
                "token_count":len(markdown_text)/4
            }

            markdown_result.append(doc_data)

        return markdown_result 
        

    # async def read_files(self) -> List:
    #     folder_paths = []

    #     for path in self.directory_path.iterdir():
    #         folder_paths.append(path)

    #     return folder_paths
    
    
    async def get_original_filename(self,db:AsyncSession,filename:str) -> str:
        get_filename = await select(FileNameStore.original_file_name).where(FileNameStore.unique_file_name == filename)
        result = await db.execute(get_filename)

        original_name = result.scalar_one_or_none()

        return original_name

    
    
    









