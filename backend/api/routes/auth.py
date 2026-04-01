# standard library
import os
from datetime import timedelta

# third-party
from fastapi import APIRouter, Depends, HTTPException

# local imports (your app)
from core.config import Settings
from core.security import create_access_token, hash_password

from schemas.auth import UserCreate, UserLogin
from schemas.token_bearer import Token

from services.auth_service.auth import authenticate_user, create_user

from api.deps.db_deps import get_db
from db.postgre.session import AsyncSession

auth_router = APIRouter()

ACCESS_CODE = os.getenv("ACCESS_CODE")


    
@auth_router.post("/register")
async def register(user:UserCreate,db:AsyncSession = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    await user

    if user:
        raise HTTPException(400, "User already exists")
    
    hashed_password = hash_password(user.password)

    new_user = create_user(user.username,user.email, hashed_password)
    
    return new_user

    
    pass 

@auth_router.post("/login")
async def login(
                user:UserLogin,
                db:AsyncSession = Depends(get_db)
            )-> Token:
   
    
    user = authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(
        {"sub": user.username},
        timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=token,token_type="bearer")

