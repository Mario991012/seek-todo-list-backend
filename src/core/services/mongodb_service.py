from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import PyMongoError
from fastapi import HTTPException
from typing import List, Optional
from bson import ObjectId

class MongoDBService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, document: dict) -> str:
        try:
            result = await self.collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")

    async def get(self, filter: Optional[dict] = None, limit: int = 100) -> List[dict]:
        try:
            cursor = self.collection.find(filter).limit(limit)
            documents = await cursor.to_list(length=limit)
            documents = [{**document, "_id": str(document["_id"])} for document in documents]
            return documents
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")

    async def get_by_id(self, document_id: str) -> Optional[dict]:
        try:
            object_id = ObjectId(document_id)
            document = await self.collection.find_one({"_id": object_id})
            document["_id"] = str(document["_id"])
            return document
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid ID format: {str(e)}")

    async def update(self, document_id: str, document: dict) -> bool:
        try:
            object_id = ObjectId(document_id)
            result = await self.collection.update_one({"_id": object_id}, {"$set": document})
            return result.modified_count > 0
        except PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")