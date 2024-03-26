from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.core.exception_handler import add_exception_handlers
from fastapi.exceptions import RequestValidationError

app = FastAPI()
add_exception_handlers(app)

# 예제 라우트 추가
@app.get("/validation_error")
async def validation_error_route():
    raise RequestValidationError([])

@app.get("/http_exception")
async def http_exception_route():
    from fastapi import HTTPException
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

@app.get("/general_exception")
async def general_exception_route():
    raise Exception("An error occurred")

@app.get("/custom_404")
async def custom_404_route():
    from starlette.exceptions import HTTPException as StarletteHTTPException
    raise StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Custom 404")

client = TestClient(app)

def test_validation_error_handler():
    response = client.get("/validation_error")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["message"] == "입력 데이터가 유효하지 않습니다."

def test_http_exception_handler():
    response = client.get("/http_exception")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Not found"

def test_general_exception_handler():
    response = client.get("/general_exception")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["message"] == "서버 오류가 발생했습니다."

def test_custom_404_handler():
    response = client.get("/custom_404")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Custom 404"
