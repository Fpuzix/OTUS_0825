# OTUS_0825

Запуск:
docker pull selenoid/chrome:124.0
docker pull selenoid/chrome:125.0
docker pull selenoid/firefox:124.0
docker pull selenoid/firefox:125.0

docker compose up --build --abort-on-container-exit --exit-code-from tests