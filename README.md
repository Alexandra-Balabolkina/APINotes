# APINotes

Приложение для создания и управления заметками с возможностью проверки орфографии и аутентификации пользователей.

## Основные функции

- Регистрация и вход пользователей с использованием JWT.
- Создание и получение заметок.
- Проверка орфографии текста заметок с помощью Яндекс Спеллера.
- Управление ошибками и возврат информации о возможных исправлениях пользователю.

## Установка и запуск

### Требования

- Python 3.7+
- Установленные библиотеки: aiohttp, asyncpg, aiohttp, bcrypt, python-jose, python-dotenv

### Запуск

```bash
docker compose up
```
## Postman

https://github.com/Alexandra-Balabolkina/APINotes/blob/develop/notes%20api.postman_collection.json


## CURL

### Регистрация пользователя
```bash
curl -X POST http://localhost:8080/registry \
     -H "Content-Type: application/json" \
     -d '{"login": "username", "password": "password"}'
```

### Вход пользователя
```bash
curl -X POST http://localhost:8080/auth \
     -H "Content-Type: application/json" \
     -d '{"login": "username", "password": "password"}'
```

### Добавление заметки
```bash
curl -X POST http://localhost:8080/notes \
     -H "Authorization: Bearer <ваш_JWT_токен>" \
     -H "Content-Type: application/json" \
     -d '{"content": "Текст заметки"}'
```

### Получение заметок
```bash
curl -X GET http://localhost:8080/notes \
     -H "Authorization: Bearer <ваш_JWT_токен>"
```