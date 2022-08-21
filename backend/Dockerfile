FROM python:3.10-slim as build
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc

RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt


FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt install -y libpango-1.0-0 \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY . .
