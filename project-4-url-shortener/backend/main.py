import secrets
import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

app = FastAPI()

# --- Настройка CORS ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- "База данных" в памяти (словарь Python) ---
# Ключ - короткий код, значение - объект с длинным URL, кликами и датой создания
url_db = {}

# --- Pydantic модели ---
class URLCreate(BaseModel):
    long_url: HttpUrl # Pydantic проверит, что это валидный URL
    custom_code: Optional[str] = Field(None, max_length=20) # Добавили необязательное поле

class URLInfo(BaseModel):
    long_url: HttpUrl
    clicks: int
    created_at: datetime.datetime

# --- Эндпоинты API ---

@app.post("/api/shorten")
def create_short_url(url_data: URLCreate, request: Request):
    """Создает короткий код для длинного URL."""
    long_url = str(url_data.long_url)
    custom_code = url_data.custom_code

    if custom_code:
        if custom_code in url_db:
            raise HTTPException(status_code=400, detail="Custom code already in use")
        short_code = custom_code
    else:
        # Генерируем случайный безопасный код
        # secrets.token_urlsafe(n) генерирует строку из n байт
        short_code = secrets.token_urlsafe(6)

        # Убедимся, что код уникален (для простого примера можно пропустить)
        while short_code in url_db:
            short_code = secrets.token_urlsafe(6)

    url_db[short_code] = {
        "long_url": long_url,
        "clicks": 0,
        "created_at": datetime.datetime.utcnow()
    }


    # Формируем полный короткий URL для ответа
    base_url = str(request.base_url)
    short_url = f"{base_url}{short_code}"

    return {"short_url": short_url, "clicks": 0}

@app.get("/{short_code}")
def redirect_to_long_url(short_code: str):
    """Ищет длинный URL по короткому коду и перенаправляет на него."""
    url_data = url_db.get(short_code)

    if not url_data:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Проверка срока действия (например, 30 дней)
    expiration_days = 30
    if datetime.datetime.utcnow() - url_data["created_at"] > datetime.timedelta(days=expiration_days):
        # Удаляем просроченную ссылку
        del url_db[short_code]
        raise HTTPException(status_code=404, detail="Short URL not found (expired)")


    url_data["clicks"] += 1
    # Выполняем HTTP 307 Temporary Redirect
    return RedirectResponse(url=url_data["long_url"])

@app.get("/api/info/{short_code}")
def get_url_info(short_code: str):
    """Возвращает информацию о короткой ссылке."""
    url_data = url_db.get(short_code)
    if not url_data:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return url_data
