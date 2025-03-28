import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional
from jose import JWTError, jwt

from src.core.services.mongodb_service import MongoDBService
from src.services.user_service import UserService
from src.core.db.mongodb.db import users_collection

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

users_db_service = MongoDBService(users_collection)
user_service = UserService(users_db_service)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        authenticated_user = await user_service.get_user(payload["sub"])
        current_time =int(time.time())
        if authenticated_user and payload["exp"] > current_time:
            return payload
        return None
    except JWTError:
        return None
