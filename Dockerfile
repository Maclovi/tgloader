from python:3.12.4-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apt-get update &&\
    apt-get install -y git &&\
    python3.12 -m pip install --upgrade pip &&\
    python3.12 -m pip install .
