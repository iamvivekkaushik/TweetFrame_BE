# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# Create app directory
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

# start command
CMD [ "uvicorn", "app.main:app", "--host=0.0.0.0"]
