# REST API

## General Information

### Base URL
- Development: `http://localhost:8000/api/v1/`

### API Documentation
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

### Authentication
The API supports the following authentication methods:
- OAuth2 (Google, GitHub)
- Token Authentication
- Session Authentication

### Response Format
All responses are returned in JSON format:
```json
{
    "status": "success",
    "data": {},
    "message": null
}
```

### Error Handling
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

!!! tip "Response Codes"
    - 200: Successful request
    - 201: Created
    - 400: Bad request
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Not found
    - 500: Internal server error

### Access Rights
- Anonymous: read-only access to public courses
- Student: access to enrolled courses
- Instructor: manage their own courses
- Administrator: full access

### Versioning
The API is versioned through the URL path:
- **/api/v1/** - current stable version

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 