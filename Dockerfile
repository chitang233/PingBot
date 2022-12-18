FROM python:slim AS builder
ENV WORKDIR /app
WORKDIR $WORKDIR
ADD . $WORKDIR
RUN apt update && apt install -y iputils-ping
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
