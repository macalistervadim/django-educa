from backend.config.settings.base import *  # noqa: F403

DEBUG = False

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CORS_ALLOW_CREDENTIALS = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
CORS_ALLOWED_ORIGINS = secrets.get_secret(
    "django",
    "DJANGO_CORS_ALLOWED_ORIGINS",
)
CSRF_TRUSTED_ORIGINS = secrets.get_secret(
    "django",
    "DJANGO_CSRF_TRUSTED_ORIGINS",
)
CORS_ALLOW_HEADERS = [
    "content-type",
    "accept",
    "origin",
    "authorization",
    "x-csrftoken",
    "cross-origin-opener-policy",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = secrets.get_secret("email", "EMAIL_HOST")
EMAIL_PORT = secrets.get_secret("email", "EMAIL_PORT")
EMAIL_USE_TLS = secrets.get_secret("email", "EMAIL_USE_TLS")
EMAIL_USE_SSL = secrets.get_secret("email", "EMAIL_USE_SSL")
EMAIL_HOST_USER = secrets.get_secret("email", "EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = secrets.get_secret("email", "EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = secrets.get_secret("email", "DEFAULT_FROM_EMAIL")
