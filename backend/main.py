import os
import sqlite3

from dotenv import load_dotenv
from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from api.routes.auth import auth_router
from api.routes.file_upload import uploader_router

from core.lifespan import lifespan
from middleware.request_logging import LoggingMiddleware


load_dotenv()

app = FastAPI(lifespan=lifespan)


SECRET_KEY = os.getenv("SECRET_KEY")

app.include_router(uploader_router)
app.include_router(auth_router)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    https_only=False,
    max_age=3600
)


@app.get("/")
async def main(request:Request):
    return RedirectResponse("/verify-access")
    # return HTTPException(status_code=400, detail="Wrong Access Code")

