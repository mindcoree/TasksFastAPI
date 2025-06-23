'use client';

import { useState, useEffect, FormEvent } from 'react';
import axios from 'axios';
import Image from 'next/image';

interface WeatherData {
  city_name: string;
  temperature: number;
  description: string;
  icon: string;
}

interface ForecastData {
  city_name: string;
  forecasts: {
    date: string;
    temperature: number;
    description: string;
    icon: string;
  }[];
}

const API_URL = 'http://localhost:8000/api';

export default function Home() {
  const [city, setCity] = useState('Almaty');
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [forecast, setForecast] = useState<ForecastData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchWeather = async (cityName: string) => {
    setLoading(true);
    setError('');
    setWeather(null);
    setForecast(null);
    try {
      const [weatherResponse, forecastResponse] = await Promise.all([
        axios.get(`${API_URL}/weather/${cityName}`),
        axios.get(`${API_URL}/forecast/${cityName}`)
      ]);
      setWeather(weatherResponse.data);
      setForecast(forecastResponse.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось загрузить данные о погоде.');
    } finally {
      setLoading(false);
    }
  };

  const fetchWeatherByCoords = async (lat: number, lon: number) => {
    setLoading(true);
    setError('');
    setWeather(null);
    setForecast(null);
    try {
      const [weatherResponse, forecastResponse] = await Promise.all([
        axios.post(`${API_URL}/weather/coords`, { lat, lon }),
        axios.get(`${API_URL}/forecast/${city}`)
      ]);
      setWeather(weatherResponse.data);
      setForecast(forecastResponse.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Не удалось загрузить данные о погоде.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Проверяем поддержку геолокации
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetchWeatherByCoords(latitude, longitude);
        },
        (err) => {
          console.error('Geolocation error:', err);
          fetchWeather('Almaty'); // Fallback to default city
        }
      );
    } else {
      fetchWeather('Almaty'); // Fallback to default city
    }
  }, []);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (city.trim()) {
      fetchWeather(city.trim());
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-200 to-purple-300 p-4">
      <div className="w-full max-w-sm bg-white/50 backdrop-blur-md p-6 rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold text-gray-800 mb-4 text-center">Погода</h1>
        <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Введите город"
            className="flex-grow p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          />
          <button type="submit" disabled={loading} className="bg-blue-500 hover:bg-blue-600 text-white font-bold p-2 rounded-lg disabled:bg-blue-300">
            {loading ? '...' : '➔'}
          </button>
        </form>

        {loading && <p className="text-center text-gray-700">Загрузка...</p>}
        {error && <p className="text-center text-red-500">{error}</p>}

        {weather && (
          <div className="flex flex-col items-center text-center text-gray-900">
            <h2 className="text-3xl font-semibold">{weather.city_name}</h2>
            <div className="flex items-center">
              <p className="text-6xl font-light">{Math.round(weather.temperature)}°C</p>
              <Image
                src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`}
                alt={weather.description}
                width={100}
                height={100}
              />
            </div>
            <p className="text-lg capitalize">{weather.description}</p>
          </div>
        )}

        {forecast && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Прогноз на 5 дней</h3>
            <div className="grid grid-cols-1 gap-4">
              {forecast.forecasts.map((day, index) => (
                <div key={index} className="flex items-center justify-between bg-white/30 p-3 rounded-lg">
                  <p>{new Date(day.date).toLocaleDateString('ru-RU', { weekday: 'short', day: 'numeric', month: 'short' })}</p>
                  <div className="flex items-center">
                    <Image
                      src={`https://openweathermap.org/img/wn/${day.icon}.png`}
                      alt={day.description}
                      width={40}
                      height={40}
                    />
                    <p>{Math.round(day.temperature)}°C</p>
                  </div>
                  <p className="capitalize">{day.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}