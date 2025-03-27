from fastapi import APIRouter, HTTPException
from bson import ObjectId
from src.core.db.mongodb.models.task import Task
from src.core.db.mongodb.db import tasks_collection
from src.core.utils.response import format_response
from src.core.common.return_codes import ReturnCode

taskRouter = APIRouter()

@taskRouter.post("/")
async def create_task(task: Task):
    task_dict = task.dict()
    task_dict["_id"] = ObjectId()
    await tasks_collection.insert_one(task_dict)
    task_dict["_id"] = str(task_dict["_id"])  # Convertir ObjectId a string
    return format_response(ReturnCode.SUCCESS, task_dict)

@taskRouter.get("/")
async def get_tasks():
    tasks = await tasks_collection.find().to_list(100)  # Limitar a 100 tareas
    for task in tasks:
        task["_id"] = str(task["_id"])
    return format_response(ReturnCode.SUCCESS, {"tasks": tasks})
