FROM python:3.11.6-alpine3.18
WORKDIR /app/api_service

COPY . /app/api_service

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi


# CMD ["poetry", "run", "uvicorn", "main:app", "--reload"]