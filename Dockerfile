ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        g++ \
        python3-dev && \
    apt-key adv --refresh-keys --keyserver keyserver.ubuntu.com || true && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY requirements.txt .

EXPOSE 11000

CMD ["python", "app.py"]