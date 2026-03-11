FROM selenium/standalone-chrome:latest

USER root

WORKDIR /app

RUN mv /usr/bin/google-chrome /usr/bin/google-chrome-orig && \
    echo '#!/bin/bash\n/usr/bin/google-chrome-orig --headless --no-sandbox --disable-dev-shm-usage "$@"' > /usr/bin/google-chrome && \
    chmod +x /usr/bin/google-chrome


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages


COPY . .

ENV PYTHONPATH=/app


CMD ["pytest", "test_web_2/", "-q", "--browser", "chrome"]
