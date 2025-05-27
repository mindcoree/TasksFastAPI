import uvicorn
from fastapi import FastAPI
from core.config import settings

app_main = FastAPI()




if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
