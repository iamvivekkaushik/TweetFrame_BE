FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

# Create app directory
WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN apk update && \
    apk add --virtual build-deps libffi-dev gcc python3-dev musl-dev && \
    apk add postgresql-dev && \
    apk add jpeg-dev && \
    apk add libjpeg && \
    apk add zlib-dev

RUN python3 -m pip install psycopg2
RUN python3 -m pip install -r requirements.txt

COPY . .

# RUN mkdir media
# RUN alembic upgrade head

# start command
CMD [ "uvicorn", "app.main:app", "--host=0.0.0.0"]
