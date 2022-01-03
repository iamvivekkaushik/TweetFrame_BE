# syntax=docker/dockerfile:1
FROM python:3.8-alpine

# Create app directory
WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN mkdir media
RUN mkdir data
RUN chmod 777 data

RUN apk update && \
    apk add --virtual build-deps libffi-dev gcc python3-dev musl-dev && \
    apk add postgresql-dev && \
    apk add jpeg-dev && \
    apk add libjpeg && \
    apk add zlib-dev

RUN python3 -m pip install psycopg2
RUN python3 -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

# start command
CMD [ "uvicorn", "app.main:app", "--reload"]
