FROM python:3.11.6-alpine3.18

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev && \
    apk add --no-cache \
    bash \
    build-base \
    curl \
    git \
    libffi-dev \
    openssl-dev && \
    pip install --no-cache-dir poetry

WORKDIR /app/parser_service

COPY poetry.lock pyproject.toml /app/parser_service/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app/parser_service

CMD ["poetry", "run", "python", "-u", "./main.py"]
