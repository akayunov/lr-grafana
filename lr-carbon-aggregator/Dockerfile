FROM ubuntu:26.04

# Добавляем python3-venv в список устанавливаемых пакетов
RUN apt-get update && apt-get install -y \
    python3-dev \
    libcairo2-dev \
    libffi-dev \
    build-essential \
    python3-pip \
    python3-venv \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение в директории /opt/venv
RUN python3 -m venv /opt/venv

# Добавляем venv в PATH, чтобы система в первую очередь использовала pip и бинарники из него
ENV PATH="/opt/venv/bin:$PATH"

# Обновляем pip и устанавливаем carbon/whisper без сохранения кэша колес
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-binary=:all: https://github.com/graphite-project/carbon/tarball/master && \
    pip install --no-cache-dir --no-binary=:all: https://github.com/graphite-project/whisper/tarball/master

WORKDIR /app
COPY conf/carbon.conf /app/carbon.conf
COPY conf/storage-schemas.conf /app/storage-schemas.conf
#COPY conf/aggregation-rules.conf /app/aggregation-rules.conf
COPY tests/metrics-reciever.py /app/metrics-reciever.py

CMD ["carbon-aggregator.py", "--nodaemon", "--config", "/app/carbon.conf",  "start"]
