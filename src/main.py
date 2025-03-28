from fastapi import FastAPI
from src.api.v1.routes.tasks import taskRouter
from src.api.v1.routes.auth import authRouter
from mangum import Mangum

app = FastAPI()

app.include_router(taskRouter, prefix="/v1/tasks", tags=["tasks"])
app.include_router(authRouter, prefix="/v1/auth", tags=["auth"])

handler = Mangum(app)