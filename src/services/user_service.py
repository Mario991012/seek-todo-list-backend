from passlib.context import CryptContext
from src.core.services.mongodb_service import MongoDBService
from src.core.db.mongodb.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_db_service: MongoDBService):
        self.user_db_service = user_db_service

    async def create_user(self, user: User):
        existing_user = await self.user_db_service.get({"username": user.username}, 1)
        if existing_user:
            return None
        
        hashed_password = pwd_context.hash(user.password)
        user_data = {"username": user.username, "password": hashed_password}
        await self.user_db_service.create(user_data)
        return user_data

    async def get_user(self, username: str):
        users = await self.user_db_service.get({"username": username}, 1)
        
        return users[0] if users else None

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if user and pwd_context.verify(password, user["password"]):
            return user
        return None
