import os
from pathlib import Path
from typing import List

from sqlalchemy import select
from db.sqlite.session import AsyncSession
from docling.document_converter import DocumentConverter
from models.sqlite.file_name_store import FileNameStore




class FileParser:
    def __init__(self,doc_converter = DocumentConverter(), directory_path:Path = Path("uploads")):
        self.converter = doc_converter
        self.directory_path = directory_path

    async def run(self) -> List[dict]:
        """ Generate a list of dictionaries of each file
        
        dict - filename
               file_content
               page_char_coount
               token_count

        """
        
        result = []

        folder_paths = await self.read_files()

        for file_path in folder_paths:
            converter = self.converter.convert(file_path)

            markdown_text = converter.document.export_to_markdown()

            doc_data = {
                "filename":file_path,
                "file_content" : markdown_text,
                "page_char_count":markdown_text.len(),
                "token_count":len(markdown_text)/4
            }

            result.append(doc_data)

        return result 
        

    async def read_files(self) -> List:
        folder_paths = []

        for path in self.directory_path.iterdir():
            folder_paths.append(path)

        return folder_paths
    
    
    async def get_original_filename(self,db:AsyncSession,filename:str) -> str:
        get_filename = await select(FileNameStore.original_file_name).where(FileNameStore.unique_file_name == filename)
        result = await db.execute(get_filename)

        original_name = result.scalar_one_or_none()

        return original_name

    
    
    









