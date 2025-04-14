# REST API

## Общая информация

### Базовый URL
- Development: `http://localhost:8000/api/v1/`

### Документация API
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

### Аутентификация
API поддерживает следующие методы аутентификации:
- OAuth2 (Google, GitHub)
- Token Authentication
- Session Authentication

### Формат ответов
Все ответы возвращаются в формате JSON:
```json
{
    "status": "success",
    "data": {},
    "message": null
}
```

### Обработка ошибок 
```json
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "errors": [
        {
            "field": "email",
            "message": "Invalid email format"
        }
    ]
}
```

### Коды ответов

- 200: Успешный запрос
- 201: Создано
- 400: Некорректный запрос
- 401: Не авторизован
- 403: Доступ запрещен
- 404: Не найдено
- 500: Внутренняя ошибка сервера

### Права доступа
- Анонимный: только чтение публичных курсов
- Студент: доступ к зачисленным курсам
- Преподаватель: управление своими курсами
- Администратор: полный доступ

### Версионирование
API версионируется через URL path:
- **/api/v1/** - текущая стабильная версия

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 