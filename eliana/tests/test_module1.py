# tests/test_module1.py
from fastapi import Depends
from fastapi.testclient import TestClient
from main import app
from utils.db_utils import db_session, delete_chart_histories, get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_chart():
    # 파이차트 생성 요청 데이터
    pie_data = {
        "user_id": "kdy987",
        "result_type": "url",
        "chart_type": "pie",
        "width": 800,
        "height": 800,
        "title": "Pie Chart 샘플",
        "labels": ["사과", "바나나", "딸기", "오렌지"],
        "sizes": [25, 35, 20, 20],
        "colors": ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
        "explode": [0.1, 0, 0.1, 0],
        "shadow": True,
        "startangle": 90,
        "autopct": "%1.1f%%",
        "pctdistance": 0.85,
        "labeldistance": 1.2,
        "wedgeprops": {"linewidth": 2, "edgecolor": "gray"},
        "textprops": {"fontsize": 14},
        "radius": 1.2,
        "counterclock": True,
        "frame": True,
        "legend_labels": ["사과 - 신선함", "바나나 - 달콤함", "딸기 - 새콤달콤함", "오렌지 - 상큼함"],
        "legend_loc": "lower center"
    }
    with db_session() as db:
        # 특정 조건에 맞는 차트 이력을 삭제합니다.
        delete_chart_histories(db)

    response = client.post("/chart",  json=pie_data)
    print(response.json())
    assert response.status_code == 200
