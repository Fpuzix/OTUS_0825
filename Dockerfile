FROM python:3.12-slim-bookworm

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver \
    firefox-esr \
    ca-certificates curl tar \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*


ENV MOZ_HEADLESS=1


RUN mv /usr/bin/chromium /usr/bin/chromium-orig && \
    printf '#!/bin/sh\nexec /usr/bin/chromium-orig --headless=new --no-sandbox --disable-dev-shm-usage --window-size=1920,1080 "$@"\n' > /usr/bin/chromium && \
    chmod +x /usr/bin/chromium


RUN set -eux; \
    GECKO_VER="$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | python -c "import sys,json; print(json.load(sys.stdin)['tag_name'])")"; \
    curl -sSL -o /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/${GECKO_VER}/geckodriver-${GECKO_VER}-linux64.tar.gz"; \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin; \
    chmod +x /usr/local/bin/geckodriver; \
    rm -f /tmp/geckodriver.tar.gz

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PYTHONPATH=/app

ENTRYPOINT ["pytest", "test_web_3/", "-q", "--alluredir=allure-results"]