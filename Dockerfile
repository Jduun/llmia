FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && \
    pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root
ENV PYTHONPATH="/app"
COPY . /app
