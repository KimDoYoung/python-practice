from fastapi import FastAPI, Response
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/setcookie")
def set_cookie(response: Response):
    response.set_cookie(key="my_cookie", value="my_value")
    response.set_cookie(key="option_cookie", value="Hello cookie...", 
                        expires=1800, 
                        max_age=3600,
                        domain="127.0.0.1", 
                        #path="/", 
                        secure=False,
                        #httponly=True, 
                        samesite="Lax"
                        )
    return {"message": "Cookie set"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)