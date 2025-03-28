from fastapi import FastAPI
from src.api.v1.routes.tasks import taskRouter
from src.api.v1.routes.auth import authRouter

app = FastAPI()

app.include_router(taskRouter, prefix="/tasks", tags=["tasks"])
app.include_router(authRouter, prefix="/auth", tags=["auth"])
