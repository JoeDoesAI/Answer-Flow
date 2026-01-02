from fastapi import APIRouter

# from services.parse_file import 

file_process = APIRouter()

@file_process.post()
async def manual_parse():
    pass
