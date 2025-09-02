import logging
import sys

import uvicorn
from core.db_setup import init_db
from fastapi import FastAPI
from contextlib import asynccontextmanager


logger = logging.getLogger(name=__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.INFO)
logger.addHandler(hdlr=handler)

for name in logging.root.manager.loggerDict:
    if name in ("uvicorn"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear
        uvicorn_logger.addHandler(hdlr=handler)
        uvicorn_logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Timepiece", lifespan=lifespan)


@app.get("/")
async def root():
    logger.info("Health check requested")
    return {"message": "Timepiece", "status": "running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
