FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH /app:$PYTHONPATH

COPY ./app /app

WORKDIR /app

# Install dependencies
RUN apt-get update -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean -y