import uvicorn
from fastapi import FastAPI
from api import router as api_router
from core.config import settings
from contextlib import asynccontextmanager
from core import db_helper
from fastapi.responses import ORJSONResponse


# Для корректного закрыть всех соединения с БД
# Освободить, ресурсы (файлы, сокеты, кэши и т.д.)
# Короче для безопасности
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup — если нужно, можно что-то подключить
    yield
    # shutdown
    await db_helper.dispose()
    print("dispose engine")


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

main_app.include_router(api_router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
