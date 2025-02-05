import os

import dotenv

dotenv.load_dotenv()


DJANGO_ENV = os.getenv("DJANGO_ENV", "development").lower()
if DJANGO_ENV == "production":
    from src.config.settings.production import *  # noqa: F403
    ALLOWED_HOSTS = ["*"]
elif DJANGO_ENV == "development":
    from src.config.settings.development import *  # noqa: F403
    ALLOWED_HOSTS = ["*"]
else:
    raise ValueError(f"Unknown environment: {DJANGO_ENV}")
