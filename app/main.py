from fastapi import FastAPI
from .routers import slackRouter, crawlRouter

app = FastAPI()
app.include_router(slackRouter.router)
app.include_router(crawlRouter.router)