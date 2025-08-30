from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("💾 App starting up...")

    yield


app = FastAPI(title="Timepiece", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Timepiece", "status": "running"}
