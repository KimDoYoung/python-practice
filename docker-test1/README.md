# FastAPI in Containers Docker + MongoDb

## 순서

mkdir app
touch app/main.py
touch README.md
python -m venv env
source env/Scripts/active
pip freeze > requirements.txt
echo "env/" > .dockerignore
echo "env/" > .gitignore

touch Dockerfile

## Dockerfile

```text
FROM python:3.9.0-alpine3.12
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app /code/app
RUN ["uvicor", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
