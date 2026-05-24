# Курсовая работа — Приложение для управления задачами

## Описание
Микросервисное приложение для управления задачами с аутентификацией и авторизацией пользователей.

## Сервисы

**Auth Service** (порт 8001) — регистрация, вход, обновление токенов, история входов, выход. Данные хранятся в PostgreSQL, невалидные токены — в Redis.

**Task Service** (порт 8003) — создание, просмотр, обновление и удаление задач. Поддерживает фильтрацию по статусу и приоритету. Доступ только по JWT токену от Auth Service.

## Быстрый старт

### 1. Запустить Auth Service
```bash
cd auth_service
cp .env.example .env
docker-compose up -d
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### 2. Запустить Task Service
```bash
cd task_service
cp .env.example .env
docker-compose up -d
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

### 3. Зарегистрироваться и получить токен
```bash
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### 4. Использовать Task API
```bash
curl -X POST http://localhost:8003/api/v1/tasks/ \
  -H "Authorization: Bearer <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My task", "priority": "high", "status": "todo"}'
```
