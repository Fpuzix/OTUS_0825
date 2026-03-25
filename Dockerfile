FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update && \
    apt-get install -y  python3 python3-pip python3-venv python3-pytest allure python3-venv&&\
    apt-get clean

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
