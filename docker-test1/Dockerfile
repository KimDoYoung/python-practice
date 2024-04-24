FROM python:3.8-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

