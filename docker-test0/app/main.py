from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World! Hongil Kim. We are the world!"}
