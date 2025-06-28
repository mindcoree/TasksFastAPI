import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator

from core.config import settings
from core.db_helper import db_helper
from core.log_config import setup_logging
from api import router as api_router
from api.common.middleware import RateLimiterMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # comment test
    yield
    await db_helper.dispose()


setup_logging()

main_app = FastAPI(
    title="Task 19 API",
    description="API for managing tasks, products, orders, and users.",
    version="1.0.0",
)


# Middleware для логирования запросов и ответов
def log_request_response_middleware(app):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger = logging.getLogger("uvicorn.access")
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code} {request.method} {request.url}")
        return response

    return app


log_request_response_middleware(main_app)


# Health check endpoint
@main_app.get("/health")
async def health():
    return {"status": "ok"}


# Prometheus metrics
Instrumentator().instrument(main_app).expose(main_app)

main_app.include_router(api_router)

main_app.add_middleware(
    RateLimiterMiddleware,
    redis_url=settings.rate_limit.redis_url,
    limit=settings.rate_limit.limit,
    window=settings.rate_limit.window
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
    )
