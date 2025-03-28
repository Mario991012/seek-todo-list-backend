from fastapi import APIRouter, HTTPException
from src.core.services.mongodb_service import MongoDBService
from src.services.user_service import UserService
from src.core.utils.jwt import create_access_token
from src.core.schemas.response import ResponseSchema, ReturnCodeEnum
from src.core.db.mongodb.models.user import User
from src.core.db.mongodb.db import users_collection

authRouter = APIRouter()
users_db_service = MongoDBService(users_collection)
user_service = UserService(users_db_service)

@authRouter.post("/register", response_model=ResponseSchema)
async def register(user: User):
    new_user = await user_service.create_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return ResponseSchema(return_code=ReturnCodeEnum.SUCCESS, data={"username": new_user["username"]})

@authRouter.post("/login", response_model=ResponseSchema)
async def login(user: User):
    authenticated_user = await user_service.authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": authenticated_user["username"]})
    return ResponseSchema(return_code=ReturnCodeEnum.SUCCESS, data={"access_token": token})
