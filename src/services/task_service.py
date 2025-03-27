from fastapi import HTTPException
from src.core.services.mongodb_service import MongoDBService
from src.core.db.mongodb.models.task import Task
from bson import ObjectId
from typing import List, Optional

class TaskService:
    def __init__(self, task_db_service: MongoDBService):
        self.task_db_service = task_db_service

    async def create_task(self, task: Task) -> str:
        try:
            task_dict = task.dict()
            task_dict["_id"] = ObjectId()
            task_id = await self.task_db_service.create(task_dict)
            task_dict["_id"] = str(task_id)
            return task_dict
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error while creating task: {str(e)}")

    async def get_tasks(self, filter: Optional[dict] = None, limit: int = 100) -> List[dict]:
        try:
            tasks = await self.task_db_service.get(filter, limit)
            return tasks
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error while fetching tasks: {str(e)}")

    async def get_task_by_id(self, task_id: str) -> dict:
        try:
            task = await self.task_db_service.get_by_id(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error while fetching task by id: {str(e)}")

    async def update_task(self, task_id: str, task: Task) -> dict:
        try:
            updated = await self.task_db_service.update(task_id, task.dict())
            if not updated:
                raise HTTPException(status_code=404, detail="Task not found")
            return {"message": "Task updated successfully"}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error while updating task: {str(e)}")
