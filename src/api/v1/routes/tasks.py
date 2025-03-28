from fastapi import APIRouter, Depends, HTTPException
from src.core.middlewares.auth_middleware import get_current_user
from src.services.task_service import TaskService
from src.core.services.mongodb_service import MongoDBService
from src.core.db.mongodb.db import tasks_collection
from src.core.schemas.response import ResponseSchema, ReturnCodeEnum
from src.core.db.mongodb.models.task import Task

taskRouter = APIRouter()

task_db_service = MongoDBService(tasks_collection)
task_service = TaskService(task_db_service)

@taskRouter.post("/", response_model=ResponseSchema)
async def create_task(task: Task, user: str = Depends(get_current_user)):
    try:
        result = await task_service.create_task(task)
        return ResponseSchema(
            return_code=ReturnCodeEnum.SUCCESS,
            data=result
        )
    except HTTPException as e:
        return ResponseSchema(
            return_code=ReturnCodeEnum.INTERNAL_ERROR,
            data=e
        )

@taskRouter.get("/", response_model=ResponseSchema)
async def get_tasks(user: str = Depends(get_current_user)):
    try:
        tasks = await task_service.get_tasks()
        return ResponseSchema(
            return_code=ReturnCodeEnum.SUCCESS,
            data=tasks
        )
    except HTTPException as e:
        return ResponseSchema(
            return_code=ReturnCodeEnum.INTERNAL_ERROR,
            data=e
        )

@taskRouter.get("/{task_id}", response_model=ResponseSchema)
async def get_task(task_id: str, user: str = Depends(get_current_user)):
    try:
        task = await task_service.get_task_by_id(task_id)
        return ResponseSchema(
            return_code=ReturnCodeEnum.SUCCESS,
            data=task
        )
    except HTTPException as e:
        return ResponseSchema(
            return_code=ReturnCodeEnum.INTERNAL_ERROR,
            data=e
        )

@taskRouter.put("/{task_id}", response_model=ResponseSchema)
async def update_task(task_id: str, task: Task, user: str = Depends(get_current_user)):
    try:
        result = await task_service.update_task(task_id, task)
        return ResponseSchema(
            return_code=ReturnCodeEnum.SUCCESS,
            data=result
        )
    except HTTPException as e:
        return ResponseSchema(
            return_code=ReturnCodeEnum.INTERNAL_ERROR,
            data=e
        )