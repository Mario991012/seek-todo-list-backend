from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    todo = "por hacer"
    in_progress = "en progreso"
    completed = "completada"

class Task(BaseModel):
    title: str
    description: str
    status: TaskStatus
    is_deleted: bool

class TaskInDB(Task):
    id: Optional[str]
