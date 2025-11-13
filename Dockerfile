FROM python:3.9.6

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        g++ \
        python3-dev \
        libffi-dev \
        libssl-dev && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6ED0E7B82643E131 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 78DBA3BC47EF2265 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F8D2585B8783D481 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 54404762BBB6E853 && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BDE6D2B9216EC7A8 && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install \
    -r requirements.txt \
    --no-binary :all:

COPY . .

EXPOSE 11000

CMD ["python", "app.py"]