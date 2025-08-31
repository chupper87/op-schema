from core.db_setup import create_db_and_tables
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Timepiece", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Timepiece", "status": "running"}
