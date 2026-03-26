FROM jenkins/jenkins:lts-jdk21

USER root

# 1. Обновляем списки
# 2. Устанавливаем ВСЕ пакеты одной командой apt-get install
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-pytest \
    allure \
    # Библиотеки для Chrome (исправляют ошибку 127)
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libglu1-mesa \
    # Браузер и драйвер
    chromium \
    chromium-driver && \
    # Чистим мусор, чтобы образ был легче
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins


#FROM python:3.12-slim
#
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
#RUN apt-get update && apt-get install -y --no-install-recommends     chromium     firefox-esr     ca-certificates     fonts-liberation     && rm -rf /var/lib/apt/lists/*
#
#WORKDIR /app
#
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . .
#
#CMD ["pytest", "-m", "api"]
