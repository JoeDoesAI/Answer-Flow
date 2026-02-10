from typing import List,Optional
from pydantic import BaseModel

from fastapi import UploadFile



class Files(BaseModel):
    files: List[UploadFile]


class IngestStatus(BaseModel):
    file_name: str
    upload_staus: bool
    file_size: int
    