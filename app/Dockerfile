FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Instalar dependencias del sistema esenciales, compiladores, pkg-config y headers de MySQL/MariaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv en la imagen
COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /uvx /bin/

WORKDIR /app

# Copiar la definición del proyecto y el lockfile para instalar dependencias reproducibles.
COPY app/pyproject.toml app/uv.lock* ./
RUN uv sync --frozen --no-install-project --no-dev

COPY ./app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./app/celery-init/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./app/celery-init/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./app/celery-init/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# Copiar el código fuente
COPY app/ .
RUN uv sync --frozen --no-dev

ENTRYPOINT ["/entrypoint"]