from fastapi import FastAPI
from internal.handlers import defaultHandler

app = FastAPI()

app.include_router(defaultHandler.router)