# 🛍️ Products API Module

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://pydantic.dev/)

## 📋 Описание

Модуль управления продуктами для FastAPI приложения. Предоставляет полный CRUD функционал для работы с товарами в системе электронной коммерции.

## 🏗️ Архитектура

Модуль следует принципам **Clean Architecture** и разделен на следующие слои:

```
api/products/
├── __init__.py           # Инициализация модуля
├── models.py            # SQLAlchemy модели
├── schemas.py           # Pydantic схемы для валидации
├── views.py             # FastAPI роуты и endpoints
├── services.py          # Бизнес-логика
├── repository.py        # Слой доступа к данным
├── dependencies.py      # FastAPI зависимости
└── exceptions.py        # Кастомные исключения
```

## 📊 Модель данных

### Product Model

```python
class Product(TimestampMix, Base):
    id: int                    # Уникальный идентификатор
    name: str                  # Название продукта (уникальное)
    description: str | None    # Описание продукта
    price: Decimal            # Цена (должна быть > 0)
    stock: int                # Количество на складе (>= 0)
    created_at: datetime      # Дата создания
    updated_at: datetime      # Дата последнего обновления
```

**Ограничения базы данных:**
- ✅ `price > 0` - цена должна быть положительной
- ✅ `stock >= 0` - количество не может быть отрицательным
- ✅ `name` - уникальное имя продукта

## 🔗 API Endpoints

### 📖 Получение продуктов

| Метод | Endpoint | Описание | Права доступа |
|-------|----------|----------|---------------|
| `GET` | `/product/{product_id}` | Получить продукт по ID | Только админы |
| `GET` | `/list-products` | Получить список всех продуктов | Только админы |

### ➕ Создание продукта

| Метод | Endpoint | Описание | Права доступа |
|-------|----------|----------|---------------|
| `POST` | `/create/product` | Создать новый продукт | Только админы |

**Тело запроса:**  
По умолчанию данные принимаются в формате формы (form-data), что удобно для работы с HTML-формами в админке.

```json
{
    "name": "iPhone 15",
    "description": "Latest Apple smartphone",
    "price": 999.99,
    "stock": 50
}
```

### ✏️ Обновление продукта

| Метод | Endpoint | Описание | Права доступа |
|-------|----------|----------|---------------|
| `PUT` | `/update/{product_id}` | Полное обновление продукта | Только админы |
| `PATCH` | `/update-partial/{product_id}` | Частичное обновление продукта | Только админы |

### 🗑️ Удаление продукта

| Метод | Endpoint | Описание | Права доступа |
|-------|----------|----------|---------------|
| `DELETE` | `/delete/{product_id}` | Удалить продукт | Только админы |

## 📝 Схемы данных

### ProductIn
```python
{
    "name": str,              # Название продукта
    "description": str | None, # Описание (опционально)
    "price": Decimal,         # Цена
    "stock": int = 0          # Количество (по умолчанию 0)
}
```

### ProductOut
```python
{
    "id": int,               # ID продукта
    "name": str,             # Название
    "description": str | None, # Описание
    "price": Decimal,        # Цена
    "stock": int,            # Количество
    "created_at": datetime,  # Дата создания
    "updated_at": datetime   # Дата обновления
}
```

### ProductUpdatePartial
```python
{
    "name": str | None,        # Название (опционально)
    "description": str | None, # Описание (опционально)
    "price": Decimal | None,   # Цена (опционально)
    "stock": int | None        # Количество (опционально)
}
```

## ⚡️ Как реализовано: работа с формами через Annotated

Для удобного и DRY-способа приёма данных из форм в FastAPI используется аннотация:

```python
from typing import Annotated
from fastapi import Form

# Пример:
async def create_product(
    product: Annotated[ProductIn, Form()]
):
    ...
```

Чтобы не писать Annotated в каждом эндпоинте, реализован вспомогательный тип/функция (например, `form_model`):

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

**Что происходит?**
- FastAPI автоматически парсит все поля ProductIn из form-data.
- Вся валидация и структура описывается только в Pydantic-схеме — не нужно дублировать поля.
- Можно использовать одни и те же схемы для body/json и для форм.

**Преимущества:**
- Чистый код: схема описывается один раз.
- Удобно для HTML-админок и API одновременно.
- Легко поддерживать и расширять.

## 🛡️ Безопасность, авторизация и аутентификация

- Все endpoints защищены зависимостью `AdminRestricted` (из папок `members` и `utils/auth`).
- Запросы к продуктам возможны только для аутентифицированных администраторов.
- Авторизация и аутентификация вынесены в отдельные модули (members, utils/auth), что делает систему гибкой и расширяемой.
- Для получения пользователя, проверки токенов и ролей используются зависимости из этих модулей.

**Пример цепочки обработки запроса:**
1. Пользователь отправляет данные (например, через HTML-форму).
2. FastAPI через form_model превращает данные в Pydantic-схему.
3. AdminRestricted проверяет, что пользователь — админ (через members + utils/auth).
4. ProductService валидирует и обрабатывает данные.
5. Ответ возвращается в виде ProductOut.

---

## ⚠️ Обработка ошибок

### Кастомные исключения
- `ProductNotFoundId` - Продукт не найден по ID
- `InvalidProductData` - Неверные данные продукта
- `ProductAlreadyExists` - Продукт с таким названием уже существует

### HTTP статусы
- `200` - Успешная операция
- `201` - Продукт создан
- `404` - Продукт не найден / Нет продуктов
- `422` - Ошибка валидации данных
- `409` - Конфликт (продукт уже существует)

## 🚀 Использование

### Создание продукта
```python
# POST /create/product
{
    "name": "Laptop Gaming",
    "description": "High-end gaming laptop",
    "price": 1299.99,
    "stock": 10
}
```

### Получение продукта
```python
# GET /product/1
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

### Частичное обновление
```python
# PATCH /update-partial/1
{
    "price": 1199.99,
    "stock": 15
}
```

## 🔄 Связи с другими модулями

- **Orders**: Продукты связаны с заказами через `OrderProductAssociation`
- **Members**: Управление доступно только администраторам
- **utils/auth**: Вся логика аутентификации и авторизации вынесена в отдельный модуль

## 🧪 Особенности реализации

### Repository Pattern
- Отделение бизнес-логики от доступа к данным
- Переиспользуемые методы работы с базой данных

### Service Layer
- Централизованная бизнес-логика
- Обработка исключений и валидация
- Транзакционность операций

### Dependency Injection
- `ProductServiceDep` - автоматическое внедрение сервиса
- `ExistingProduct` - валидация существования продукта
- `AdminRestricted` - проверка прав доступа

## 📈 Масштабируемость

Архитектура модуля позволяет легко добавлять новые функции:
- 🏷️ Категории продуктов
- 🖼️ Изображения продуктов
- ⭐ Рейтинги и отзывы
- 🏪 Мультивендорность
- 📊 Аналитика продаж

## 🤝 Контрибьюторы

Разработано [@mindcoree](https://github.com/mindcoree) в рамках задания FastAPI проекта.

---

*Данный модуль является частью более крупной системы управления заказами и продуктами.*