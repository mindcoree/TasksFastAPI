import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.db_helper import db_helper
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
    )
