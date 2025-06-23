import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

# Загружаем переменные окружения из .env файла
load_dotenv()

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

# --- Получение API ключа и базовых URL ---
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


# --- Модель для координат ---
class Coords(BaseModel):
    lat: float
    lon: float


# --- Эндпоинт для текущей погоды по городу ---
@app.get("/api/weather/{city}")
async def get_weather(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_BASE_URL, params=params)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    if response.status_code != 200:
        error_detail = response.json().get("message", "Error fetching weather data")
        raise HTTPException(status_code=response.status_code, detail=error_detail)

    data = response.json()
    relevant_data = {
        "city_name": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }

    return relevant_data


# --- Эндпоинт для текущей погоды по координатам ---
@app.post("/api/weather/coords")
async def get_weather_by_coords(coords: Coords):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured")

    params = {
        "lat": coords.lat,
        "lon": coords.lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_BASE_URL, params=params)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Location not found")
    if response.status_code != 200:
        error_detail = response.json().get("message", "Error fetching weather data")
        raise HTTPException(status_code=response.status_code, detail=error_detail)

    data = response.json()
    relevant_data = {
        "city_name": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }

    return relevant_data


# --- Эндпоинт для прогноза на 5 дней ---
@app.get("/api/forecast/{city}")
async def get_forecast(city: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(FORECAST_BASE_URL, params=params)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    if response.status_code != 200:
        error_detail = response.json().get("message", "Error fetching forecast data")
        raise HTTPException(status_code=response.status_code, detail=error_detail)

    data = response.json()
    # Получаем прогноз на 12:00 каждого дня
    daily_forecasts = []
    seen_dates = set()

    for forecast in data["list"]:
        date = forecast["dt_txt"].split(" ")[0]
        time = forecast["dt_txt"].split(" ")[1]
        if time.startswith("12:00") and date not in seen_dates:
            seen_dates.add(date)
            daily_forecasts.append({
                "date": date,
                "temperature": forecast["main"]["temp"],
                "description": forecast["weather"][0]["description"],
                "icon": forecast["weather"][0]["icon"]
            })

    return {
        "city_name": data["city"]["name"],
        "forecasts": daily_forecasts[:5]  # Ограничиваем до 5 дней
    }