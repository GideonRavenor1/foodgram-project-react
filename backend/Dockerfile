FROM python:3.10-slim as build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY --from=build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY . .
