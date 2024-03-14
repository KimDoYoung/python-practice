# tests/test_module1.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_function1():
    assert True


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    #assert response.json() == {"message": "Hello World"}    