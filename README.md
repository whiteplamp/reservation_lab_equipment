# Лабораторное оборудование - Система бронирования

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-✓-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-✓-blue?logo=postgresql)

Система управления и бронирования лабораторного оборудования с REST API на FastAPI и PostgreSQL.

## Содержание
- [Быстрый старт](#-быстрый-старт)
- [Доступ к API](#-доступ-к-api)
- [Технологии](#-технологии)
- [Документация API](#-документация-api)
- [Тестирование](#-тестирование)
- [Конфигурация](#-конфигурация)
- [Структура проекта](#-структура-проекта)
- [Участие в разработке](#-участие-в-разработке)
- [Лицензия](#-лицензия)

## 🚀 Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- Python 3.9+

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/lab-equipment-booking.git
cd lab-equipment-booking
```

Создайте файл .env:

```bash
cp .env.example .env
```

Запустите сервисы:

```bash
docker-compose up -d --build
```

🌐 Доступ к API
API будет доступно по адресу:
http://localhost:8000/docs
(Swagger UI с документацией)

🛠 Технологии
Backend: FastAPI (Python 3.9)

База данных: PostgreSQL 13

ORM: Peewee

Контейнеризация: Docker

📚 Документация API
Основные endpoint'ы:
Метод	Endpoint	Описание
GET	/equipment/	Список оборудования
POST	/equipment/	Бронирование оборудования
GET	/equipment/{id}	Информация об оборудовании

⚙️ Конфигурация
Файл .env:
```
# PostgreSQL
DB_NAME=equipment_db
DB_USER=app_user
DB_PASS=secure_password
DB_HOST=postgres
DB_PORT=5432
```

Просто указываете логин, пароль, пользователя, бд автоматически разворачивается с этими данными
