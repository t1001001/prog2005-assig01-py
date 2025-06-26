from fastapi import FastAPI
from internal.handlers import defaultHandler, infoHandler, populationHandler,statusHandler

app = FastAPI()

app.include_router(defaultHandler.router)
app.include_router(infoHandler.router)
app.include_router(populationHandler.router)
app.include_router(statusHandler.router)