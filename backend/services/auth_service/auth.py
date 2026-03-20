# from passlib.context import CryptContext
# from core.config import Settings

from models.postgre.user import User
# from pwdlib import PasswordHash
# password_hash = PasswordHash.recommended()

# ACCESS_TOKEN_EXPIRE_MINUTES = 3600

# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")



# def authenticate_user(db, email: str, password: str):
#     user = ge(db, email)
#     if not user:
#         verify_password(password, DUMMY_HASH)
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# async def get_user(db: AsyncSession, email: int):
#     result = await db.execute(
#         select(User).where(User.id == user_id)
#     )
#     return result.scalar_one_or_none()


# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt.exceptions import InvalidTokenError
# import jwt

# from fastapi import Depends, FastAPI, HTTPException, status

# from datetime import datetime, timedelta, timezone
# from typing import Annotated

# from api.deps.db_deps import get_db


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, 

from models.postgre.user import User
from core.security import verify_password


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

async def create_user(db, username:str, email:str, hashed_password:str):
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    
    await db.add(new_user)
    db.commit()
    db.refresh(new_user)