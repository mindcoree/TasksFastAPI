# 📘 Сборник заданий по FastAPI

Добро пожаловать в учебный репозиторий **FastAPI Tasks**! 🎉  
Этот проект создан для изучения разработки REST API с использованием **FastAPI**. Здесь собраны практические задания, которые помогут освоить создание API: от простых эндпоинтов до аутентификации и защиты маршрутов.

**Целевая аудитория**: Студенты, начинающие разработчики и все, кто хочет изучить FastAPI.

---

## 🎯 Цели репозитория

- Познакомить с основами FastAPI и его преимуществами.
- Научить организовывать модульную структуру проекта.
- Показать интеграцию с базой данных и аутентификацией.
- Дать практические примеры для создания, тестирования и деплоя API.

---

## 📂 Структура проекта

Каждое задание находится в отдельной папке с кодом и описанием.

```
TasksFastAPI/
├── task_1_notes/         # API для заметок
├── task_2_auth/          # Регистрация и логин
├── task_3_hashing/       # Хеширование паролей
├── task_4_jwt/           # Внедрение JWT
├── task_5_protected/     # Защита эндпоинтов
├── requirements.txt      # Зависимости (для pip)
├── pyproject.toml        # Конфигурация Poetry
└── README.md             # Документация
```

### ✅ Задания

| № | Название                     | Описание                                                                 | Эндпоинты                     | Особенности                              |
|---|------------------------------|--------------------------------------------------------------------------|-------------------------------|------------------------------------------|
| 1 | API для заметок             | Простое API для создания и получения заметок                             | `POST /notes`, `GET /notes`   | Введение в FastAPI, Pydantic, CRUD       |
| 2 | Регистрация и логин         | Регистрация пользователей и авторизация по логину                        | `POST /register`, `POST /login` | PostgreSQL, Pydantic валидация         |
| 3 | Хеширование паролей         | Безопасное хранение паролей с использованием bcrypt                      | -                             | Интеграция passlib, безопасность         |
| 4 | Внедрение JWT               | Создание и проверка JWT-токенов для авторизации                          | `POST /token`                 | PyJWT, токены                           |
| 5 | Защита эндпоинтов           | Ограничение доступа к приватным маршрутам для неавторизованных пользователей | -                             | Dependencies в FastAPI                  |

---

## 🚀 Быстрый старт

### 1. Требования
- Python 3.7+
- Poetry (рекомендуется)
- PostgreSQL
- Git

### 2. Клонирование репозитория
```bash
git clone https://github.com/mindcoree/TasksFastAPI.git
cd TasksFastAPI
```

### 3. Установка Poetry
Если Poetry не установлен:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Добавьте Poetry в PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 4. Установка зависимостей
С Poetry:
```bash
poetry install
```
Или с pip:
```bash
pip install -r requirements.txt
```

### 5. Настройка базы данных
1. Установите и запустите PostgreSQL.
2. Создайте базу данных:
   ```bash
   createdb tasks_fastapi
   ```
3. Настройте .env :
   ```python
   NOTE_CONFIG__DB__URL=postgresql+asyncpg://mindcore:mindcore@localhost:5432/note
   ```

### 6. Настройка миграций с Alembic
1. Установите Alembic:
   ```bash
   poetry add alembic
   ```
2. Инициализируйте Alembic для асинхронного SQLAlchemy:
   ```bash
   alembic init -t async migrations
   ```
3. Создайте миграцию для существующих моделей:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```
4. Примените миграции к базе данных:
   ```bash
   alembic upgrade head
   ```

### 7. Запуск проекта
Запустите сервер для нужного задания:
```bash
cd task_1_notes
uvicorn app.main:app --reload
```
Откройте в браузере:
- API: `http://127.0.0.1:8000`
- Документация: `http://127.0.0.1:8000/docs`

---

## 🛠 Технологии

- **FastAPI**: Фреймворк для создания высокопроизводительных API.
  ```bash
  poetry add fastapi
  ```
- **Uvicorn**: ASGI-сервер для запуска FastAPI.
  ```bash
  poetry add "uvicorn[standard]"
  ```
- **Pydantic**: Валидация данных и сериализация (с поддержкой проверки email).
  ```bash
  poetry add "pydantic[email]"
  ```
- **Pydantic-settings**: Управление настройками приложения через переменные окружения.
  ```bash
  poetry add pydantic-settings
  ```
- **SQLAlchemy**: ORM для работы с PostgreSQL.
  ```bash
  poetry add sqlalchemy
  ```
- **Alembic**: Управление миграциями базы данных.
  ```bash
  poetry add alembic
  ```
- **PyJWT**: Создание и проверка JWT-токенов.
  ```bash
  poetry add pyjwt
  ```
- **Passlib**: Хеширование паролей (bcrypt).
  ```bash
  poetry add passlib[bcrypt]
  ```
- **PostgreSQL**: Реляционная база данных (устанавливается отдельно).
  - Установите PostgreSQL: https://www.postgresql.org/download/
- **Poetry**: Управление зависимостями и виртуальным окружением.
  - Уже установлен на шаге 3 в "Быстром старте".

---

## 🧪 Тестирование

Тесты находятся в папке `tests/` каждого задания. Для запуска:
1. Активируйте Poetry:
   ```bash
   poetry shell
   ```
2. Установите pytest:
   ```bash
   poetry add pytest
   ```
3. Запустите тесты:
   ```bash
   pytest
   ```

---

## 🚢 Деплой

Для развертывания (Heroku, Render, VPS):
1. Создайте `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. Настройте переменные окружения (например, `DATABASE_URL`).
3. Используйте Docker:
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . .
   RUN pip install poetry
   RUN poetry install
   CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

---

## 📚 Ресурсы

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [FastAPI Users](https://github.com/fastapi-users/fastapi-users)
- [Real Python: FastAPI](https://realpython.com/fastapi-python-web-apis/)
- YouTube: “FastAPI Tutorial: Build a REST API”
- GitHub: Поиск “fastapi boilerplate”

---

## 🤝 Как внести вклад

1. Форкните репозиторий.
2. Создайте ветку: `git checkout -b feature/new-task`.
3. Добавьте изменения и тесты.
4. Отправьте Pull Request.

---

## 📬 Контакты

- **GitHub**: [mindcoree](https://github.com/mindcoree)
- **Email**: tim.042007@mail.ru

**Начните создавать API с FastAPI уже сегодня! 🚀**
