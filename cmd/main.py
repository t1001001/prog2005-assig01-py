from fastapi import FastAPI
from internal.handlers import defaultHandler, statusHandler, infoHandler

app = FastAPI()

app.include_router(defaultHandler.router)
app.include_router(infoHandler.router)
app.include_router(statusHandler.router)