import uvicorn
from fastapi import FastAPI
from Timur_Medikhanov_Task_16.core.config import settings
from Timur_Medikhanov_Task_16.api import router as api_router
from fastapi.responses import ORJSONResponse

app_main = FastAPI(
    default_response_class=ORJSONResponse,
)

app_main.include_router(api_router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
