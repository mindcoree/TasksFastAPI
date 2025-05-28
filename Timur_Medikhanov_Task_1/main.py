import uvicorn
from fastapi import FastAPI
from core.config import settings
from Timur_Medikhanov_Task_1.api import router as api_router

app_main = FastAPI()

app_main.include_router(api_router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
