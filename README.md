# OTUS_0825

Запуск:
docker build -t test_web_3 .

docker run --rm -it --shm-size=2g
    -v ${PWD}\allure-results:/app/allure-results test_web_3
    --browser firefox
