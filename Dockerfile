FROM python:latest AS builder
ENV WORKDIR /app
WORKDIR $WORKDIR
ADD . $WORKDIR
RUN pip install --upgrade --no-cache-dir pip && pip install --no-cache-dir -r requirements.txt
