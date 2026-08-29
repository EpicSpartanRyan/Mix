FROM python:3.14-slim

# Instalar dependencias del sistema esenciales, compiladores, pkg-config y headers de MySQL/MariaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY app/requirements.txt .

# Instalar PyTorch estándar y el resto de dependencias del stack
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio && \
    pip install --no-cache-dir -r requirements.txt


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

WORKDIR /app

# Copiar el código fuente
COPY app/ .


ENTRYPOINT ["/entrypoint"]