FROM python:3.14-slim

# Instalar dependencias del sistema esenciales, compiladores, pkg-config y headers de MySQL/MariaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY app/requirements.txt .

# Instalar PyTorch estándar y el resto de dependencias del stack
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision torchaudio && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app/ .

# En lugar de solo ejecutar y salir, puedes usar un comando que mantenga el contenedor activo:
CMD ["python", "-u", "tests/test_emqx.py"]