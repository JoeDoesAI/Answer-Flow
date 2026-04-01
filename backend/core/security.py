from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from core.config import Settings


SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.HASHING_ALGORITHM

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def hash_password(password):
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)