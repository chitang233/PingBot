FROM python:slim AS builder
ENV WORKDIR /app
WORKDIR $WORKDIR
ADD . $WORKDIR
RUN apt update && apt install -y iputils-ping bind9-dnsutils \
    && rm -rf /var/cache /var/log /var/lib/apt/lists
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
