# Курсовая работа — Приложение для управления задачами

## Описание
Микросервисное приложение для управления задачами с аутентификацией и авторизацией пользователей.

## Архитектура

Auth Service (port 8001) --JWT--> Task Service (port 8003)
      |                                    |
PostgreSQL + Redis                    PostgreSQL
(port 5434/6380)                     (port 5436)

## Сервисы

### 1. Auth Service (порт 8001)
Аутентификация и авторизация пользователей на базе JWT.
[Подробнее](./auth_service/README.md)

### 2. Task Service (порт 8003)
Управление задачами пользователя. Требует JWT токен.
[Подробнее](./task_service/README.md)

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
