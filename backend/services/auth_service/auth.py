from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import verify_password
from models.postgre.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 3600



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

async def create_user(db, firstname:str, lastname:str, email:str, hashed_password:str):
    new_user = User(first_name=firstname, last_name= lastname, email=email, hashed_password=hashed_password)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


