from fastapi import FastAPI
from src.api.v1.routes.tasks import taskRouter

app = FastAPI()

app.include_router(taskRouter, prefix="/tasks", tags=["tasks"])
