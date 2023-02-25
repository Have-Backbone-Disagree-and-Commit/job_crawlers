from fastapi import FastAPI
from .routers import seekRouter, programmersRouter

app = FastAPI()
app.include_router(seekRouter.router)
app.include_router(programmersRouter.router)