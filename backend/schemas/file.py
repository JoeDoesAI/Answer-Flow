from typing import List
from pydantic import BaseModel


class UploadResponse(BaseModel):
    files_status: List[dict]


# class IngestStatus(BaseModel):
#     file_name: str
#     upload_staus: list
#     file_size: int
    