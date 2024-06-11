FROM python:3.11.6-alpine3.18
WORKDIR /app/api_service

RUN apk update
RUN apk add --virtual build-deps
RUN apk add gcc 
RUN apk add python3-dev
RUN apk add musl-dev
RUN apk add postgresql-dev
RUN pip install poetry

COPY . /app/api_service
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
