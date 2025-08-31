from core.db_setup import init_db
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Timepiece", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Timepiece", "status": "running"}
