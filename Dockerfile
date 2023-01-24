FROM python:slim AS builder
ENV WORKDIR /app
WORKDIR $WORKDIR
ADD . $WORKDIR
RUN apt update && apt install -y iputils-ping net-utils \
    && rm -rf /var/cache /var/log /var/lib/apt/lists
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
