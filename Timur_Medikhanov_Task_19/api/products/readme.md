# 🛍️ Products API Module

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://pydantic.dev/)

---

## 📋 Описание

Модуль управления продуктами для FastAPI-приложения. Предоставляет полный CRUD-функционал для работы с товарами в системе: создание, просмотр, обновление и удаление продуктов. Все действия доступны только администраторам, реализована строгая авторизация и аутентификация.

Данный модуль разработан по принципам **Clean Architecture**, что обеспечивает чистоту кода, удобство сопровождения и масштабируемость. Модуль легко интегрируется в более крупные проекты и может быть расширен дополнительными возможностями (категории, изображения, аналитика и т.д.).

---

## 🏗️ Архитектура

Структура модуля:

```
api/products/
├── __init__.py           # Инициализация модуля
├── models.py             # SQLAlchemy модели (таблица продуктов)
├── schemas.py            # Pydantic-схемы для валидации входных/выходных данных
├── views.py              # FastAPI роуты и endpoints
├── services.py           # Бизнес-логика (ProductService)
├── repository.py         # Репозиторий для работы с БД (ProductRepository)
├── dependencies.py       # Зависимости FastAPI (DI)
└── exceptions.py         # Кастомные исключения для обработки ошибок
```

**Ключевые принципы:**
- **Separation of Concerns:** Каждый слой отвечает за свою зону ответственности.
- **Dependency Injection:** Для всех сервисов, репозиториев и зависимостей.
- **Repository Pattern:** Легко заменить источник данных (например, перейти с SQLite на Postgres).

---

## 📊 Модель данных

### Product

```python
class Product(TimestampMix, Base):
    id: int                     # Уникальный идентификатор
    name: str                   # Название продукта (уникальное)
    description: str | None     # Описание продукта
    price: Decimal              # Цена (> 0)
    stock: int                  # Количество на складе (>= 0)
    created_at: datetime        # Дата создания
    updated_at: datetime        # Дата последнего обновления
```

**Ограничения:**
- `price > 0` — цена должна быть положительной
- `stock >= 0` — количество не может быть отрицательным
- `name` — уникальность на уровне БД

---

## 🔗 API Endpoints

| Метод   | Endpoint                      | Описание                        | Доступ           |
|---------|-------------------------------|----------------------------------|------------------|
| GET     | `/product/{product_id}`       | Получить продукт по ID           | Только админы    |
| GET     | `/list-products`              | Получить список всех продуктов   | Только админы    |
| POST    | `/create/product`             | Создать новый продукт            | Только админы    |
| PUT     | `/update/{product_id}`        | Полное обновление продукта       | Только админы    |
| PATCH   | `/update-partial/{product_id}`| Частичное обновление продукта    | Только админы    |
| DELETE  | `/delete/{product_id}`        | Удалить продукт                  | Только админы    |

**Пример запроса на создание продукта:**
```json
{
    "name": "iPhone 15",
    "description": "Latest Apple smartphone",
    "price": 999.99,
    "stock": 50
}
```

---

## 📝 Схемы данных

### Входные схемы

#### ProductIn

```python
{
    "name": str,                 # Название продукта
    "description": str | None,   # Описание (необязательно)
    "price": Decimal,            # Цена
    "stock": int = 0             # Количество (по умолчанию 0)
}
```

#### ProductUpdatePartial

```python
{
    "name": str | None,
    "description": str | None,
    "price": Decimal | None,
    "stock": int | None
}
```

### Выходная схема

#### ProductOut

```python
{
    "id": int,
    "name": str,
    "description": str | None,
    "price": Decimal,
    "stock": int,
    "created_at": datetime,
    "updated_at": datetime
}
```

---

## ⚡️ Работа с формами через Annotated

Для поддержки одновременной работы с API (json body) и HTML-формами используется следующий подход:

```python
from typing import Annotated
from fastapi import Form

async def create_product(
    product: Annotated[ProductIn, Form()]
):
    ...
```

Чтобы не дублировать описание схем, реализован вспомогательный тип/функция (`form_model`), который автоматически превращает поля Pydantic-схемы в параметры формы. Пример использования:
```python
from type.annotated import form_model

@router.post("/create/product")
async def create_product(
    restricted: AdminRestricted,
    product: form_model(ProductIn),
    service: ProductServiceDep
):
    ...
```

**Преимущества:**
- Вся структура данных описывается единожды — в Pydantic-схемах.
- Нет необходимости создавать отдельные схемы для формы и JSON.
- Удобно для интеграции с административными панелями и API-клиентами.

---

## 🛡️ Безопасность, авторизация и аутентификация

- Все endpoints защищены зависимостью `AdminRestricted` (см. папки `members` и `utils/auth`).
- Доступ к продуктам имеют только аутентифицированные администраторы.
- Авторизация и аутентификация реализованы в отдельных модулях, что позволяет легко масштабировать и изменять логику доступа.

**Цепочка обработки запроса:**
1. Пользователь отправляет данные (JSON или form-data).
2. FastAPI преобразует их в Pydantic-схему.
3. Зависимость `AdminRestricted` проверяет права пользователя.
4. Сервис обрабатывает бизнес-логику.
5. Клиенту возвращается валидированный результат.

---

## ⚠️ Обработка ошибок

### Кастомные исключения

- `ProductNotFoundId` — продукт не найден по ID
- `InvalidProductData` — некорректные данные продукта
- `ProductAlreadyExists` — продукт с таким названием уже существует

### HTTP статусы

- `200` — ОК
- `201` — Продукт создан
- `404` — Не найдено
- `422` — Ошибка валидации
- `409` — Конфликт (уже существует)

---

## 🚀 Примеры использования

**Создать продукт**
```http
POST /create/product
Content-Type: application/json

{
    "name": "Laptop Gaming",
    "description": "High-end gaming laptop",
    "price": 1299.99,
    "stock": 10
}
```

**Получить продукт**
```http
GET /product/1
```
**Ответ:**
```json
{
    "id": 1,
    "name": "Laptop Gaming",
    "description": "High-end gaming laptop",
    "price": 1299.99,
    "stock": 10,
    "created_at": "2025-06-12T10:05:54",
    "updated_at": "2025-06-12T10:05:54"
}
```

**Частичное обновление**
```http
PATCH /update-partial/1
Content-Type: application/json

{
    "price": 1199.99,
    "stock": 15
}
```

---

## 🔄 Связи с другими модулями

- **Orders:** Продукты связаны с заказами через `OrderProductAssociation`.
- **Members:** Доступ к управлению — только у админов.
- **utils/auth:** Вся логика аутентификации и авторизации вынесена в отдельный модуль для переиспользования.

---

## 🧪 Особенности реализации

- **Repository Pattern:** Четкое разделение бизнес-логики и работы с БД.
- **Service Layer:** Централизованное место для бизнес-правил, обработки ошибок и транзакций.
- **Dependency Injection:** Использование FastAPI-зависимостей для внедрения сервисов и репозиториев.
- **Валидация:** Используются Pydantic-схемы для строгой проверки данных на всех слоях.
- **Обработка ошибок:** Кастомные исключения с удобными описаниями и статусами HTTP.

---

## 📈 Масштабируемость

Модуль легко расширяется:
- 🏷️ Категории и фильтры для продуктов
- 🖼️ Загрузка изображений
- ⭐ Рейтинги/отзывы
- 🏪 Поддержка мультивендорности
- 📊 Отчеты и аналитика по продажам

---

## 🤝 Контрибьюторы

Разработано [@mindcoree](https://github.com/mindcoree) в рамках учебного проекта по FastAPI.

---

*Данный модуль является частью системы управления заказами и продуктами. Может быть интегрирован в любые FastAPI-проекты.*
