<h2>TweetFrames (Backend)</h2>

<h4>Personalize your Twitter Profile with custom Frames.</h4>

This Project is built using Python's [Fast API](https://fastapi.tiangolo.com/) Framework.

___

## ⚙️ Installation

Install the dependencies using poetry

```bash
poetry install
```

## 👨‍💻 Running the Project

First make sure to add env variables. Then use alembic command to run the migrations.

```bash
alembic upgrade head
```

Run the server.

```bash
uvicorn app.main:app --reload
```


## Creating a new migration

Use the alembic command to generate a new migration.

```bash
alembic revision --autogenerate -m "migration-name"
```
