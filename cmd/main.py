from fastapi import FastAPI
from internal.handlers import defaultHandler, statusHandler

app = FastAPI()

app.include_router(defaultHandler.router)
app.include_router(statusHandler.router)