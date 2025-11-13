FROM python:3.9-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        g++ \
        python3-dev \
        libffi-dev \
        libssl-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install \
    -r requirements.txt \
    --no-binary :all:

COPY . .

EXPOSE 11000

CMD ["python", "app.py"]