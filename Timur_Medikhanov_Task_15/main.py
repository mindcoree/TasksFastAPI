import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.db_helper import db_helper
from core.config import settings
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # comment test
    yield
    await db_helper.dispose()


main_app = FastAPI()


main_app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
    )
