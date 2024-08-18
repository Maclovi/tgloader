FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY pyproject.toml .
RUN pip install uv && uv pip install --no-cache --system .

COPY . .

RUN pip install uv && uv pip install --no-cache --system -e .
