from pydantic import BaseModel
from typing import Optional
from enum import Enum
from typing import Optional
from datetime import datetime

class TaskStatus(str, Enum):
    todo = "por hacer"
    in_progress = "en progreso"
    completed = "completada"
    deleted = "borrado"

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo

class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus
    created_at: datetime

class TaskInDB(Task):
    id: Optional[str]
