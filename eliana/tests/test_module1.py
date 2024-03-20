# tests/test_module1.py
import json
import os
from fastapi import Depends
from fastapi.testclient import TestClient
from main import app
from utils.db_utils import db_session, delete_chart_histories, get_db

client = TestClient(app)

def load_test_data(filename):
    """테스트 데이터 파일을 읽어서 Python 객체로 변환합니다."""
    current_dir = os.path.dirname(__file__)
    path = os.path.join(current_dir, 'data', filename)
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_chart():
    with db_session() as db:
        # 특정 조건에 맞는 차트 이력을 삭제합니다.
        delete_chart_histories(db)

    file_names = ('bar','line','pie')
    for file_name in file_names:
        data = load_test_data(f'{file_name}.json')
        response = client.post("/chart",  json=data)
        assert response.status_code == 200
