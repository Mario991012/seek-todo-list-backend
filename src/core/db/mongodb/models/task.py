from pydantic import BaseModel
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class TaskStatus(str, Enum):
    todo = "por hacer"
    in_progress = "en progreso"
    completed = "completada"

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus

class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus

class TaskInDB(Task):
    id: Optional[str]
