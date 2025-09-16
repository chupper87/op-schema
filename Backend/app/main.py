import uvicorn
from .core.db_setup import init_db
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.logger import logger
from .routers import auth, user, customer


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Timepiece API...")
    init_db()
    yield


app = FastAPI(title="Timepiece", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(customer.router)


@app.get("/")
async def root():
    return {"message": "Timepiece", "status": "running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
