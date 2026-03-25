FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update && \
    apt-get install -y  python3 python3-pip python3-venv python3-pytest allure python3-venv&&\
    apt-get clean \
    # Зависимости для Chrome/Chromedriver
#    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
#    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
#    libgbm1 libasound2 libpango-1.0-0 libpangocairo-1.0-0 \
    # Сам браузер (без него драйвер не запустится)
    chromium chromium-driver && \
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
