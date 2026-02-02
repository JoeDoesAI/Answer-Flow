import os
from pathlib import Path
from typing import List

from docling.document_converter import DocumentConverter
from models.sqlite.file_name_store import FileNameStore


script_location = Path(__file__).parent.parent



# This path will always resolve correctly to your uploads folder
uploads_path = script_location /  "uploads"

class DocumentParser:
    def __init__(self,doc_converter = DocumentConverter(), directory_path:Path = Path(uploads_path)):
        self.converter = doc_converter
        self.directory_path = directory_path
        

    async def read_files(self) -> List[dict]:
        folder_paths = []
        
        for path in self.directory_path.iterdir():
            await folder_paths.append(path)

        return folder_paths
    
    
    async def get_original_filename(self):
        pass

    
    async def convert_docs(self) -> List[dict]:
        """ Generate a list of dictionaries of each file
        
        dict - filename
               file_content
               page_char_coount
               token_count

        """
        
        result = []

        for file_path in self.read_files():
            result = self.converter.convert(file_path)

            markdown_text = await result.document.export_to_markdown()

            file = {
                "filename":file_path,
                "file_content" : markdown_text,
                "page_char_count":markdown_text.len(),
                "token_count":len(markdown_text)/4
            }

            result.append(file)

        return result  
    









