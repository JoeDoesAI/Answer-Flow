from pathlib import Path

from fastapi import UploadFile


class DocumentValidator:
    def __inti__(self, max_size:int = 20 * 1024 * 1024):
        self.allowed_exttensions = [".pdf",".txt",".json"]
        self.max_size = max_size
        
    async def validate_file(self,file:UploadFile) -> dict:
        result = {"valid": True, "errors":[]}

        
        #check for file
        if file.filename == "" or file.filename.strip() == "":
            result["valid"] = False
            result["errors"].append("no file selected")

            return result
        
        #check file extension

        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in self.allowed_exttensions:
            result["valid"] = False
            result["errors"].append("The file extension {file_ext} not allowwed")

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


        

