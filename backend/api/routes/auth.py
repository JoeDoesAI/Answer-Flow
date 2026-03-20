import os
from typing import Annotated
from fastapi import Depends,HTTPException
from fastapi import APIRouter,Request
from fastapi.security import OAuth2PasswordRequestForm

from deps.db_deps import get_db
from db.postgre.session import AsyncSession
from services.auth_service.auth import authenticate_user,create_user
from core.security import create_access_token,hash_password
from schemas.auth import UserCreate, UserLogin

auth_router = APIRouter()

ACCESS_CODE = os.getenv("ACCESS_CODE")

@auth_router.post("/verify-access")
async def verify_access(request: Request):
    # request.session.get("access_code")
    access_code = "FLOW56" #later change to the top

    if access_code == ACCESS_CODE:
        request.session["authorized"] = True
        #RedirectResponse("/home")

        return {"logedin":"access-granted"}
    
@auth_router.post("/register")
async def register(user:UserCreate,db:AsyncSession = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)

    if user:
        raise HTTPException(400, "User already exists")
    
    hashed_password = hash_password(user.password)

    create_user(user.username,user.email, hashed_password)
    
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
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}

