FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends locales gettext && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir uv

COPY ../.. /app/

RUN uv venv --python=/usr/local/bin/python3 /app/.venv && \
    uv pip install ".[dev]"

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "backend.config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]