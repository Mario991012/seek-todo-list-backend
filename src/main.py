from fastapi import FastAPI
from src.api.v1.routes.tasks import taskRouter
from src.api.v1.routes.auth import authRouter
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(taskRouter, prefix="/v1/tasks", tags=["tasks"])
app.include_router(authRouter, prefix="/v1/auth", tags=["auth"])
