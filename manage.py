#!/usr/bin/env python
import os
import sys
from typing import Any


def main() -> Any:
    """Run administrative tasks."""
    settings_module = os.getenv(
        "DJANGO_SETTINGS_MODULE",
        "src.config.settings.production",
    )
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?",
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
