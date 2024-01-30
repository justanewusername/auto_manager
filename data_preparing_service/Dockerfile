FROM python:3.11.6-alpine3.18
WORKDIR /app/data_preparing_service

COPY . /app/data_preparing_service

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi


CMD ["poetry", "run", "python", "./main.py"]