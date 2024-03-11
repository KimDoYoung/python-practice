import json
import os
from fastapi import APIRouter, Depends

from model.ChartRequest import BarChartRequest
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.db_utils import ChartHistory, Session, add_chart_history, calculate_request_hash, get_db

from utils.file_utils import get_file_path
#from models import Item

router = APIRouter()

@router.post("/chart/bar")
async def chart_bar(request: BarChartRequest, db: Session = Depends(get_db)):
    # hash를 구해서 
    request_hash = calculate_request_hash(request);
    chart_history = db.query(ChartHistory).filter(ChartHistory.json_hash == request_hash).first()

    # 존재하면 url을 리턴
    if chart_history:
        return {"url": chart_history.url}
        
    # 파일 경로 생성
    file_path = get_file_path(request.width, request.height)

    # 차트 생성 로직 (matplotlib 사용)
    plt.figure(figsize=(request.width / 100, request.height / 100))

    if request.title:
        plt.title(request.title)
    if request.x_label:
        plt.xlabel(request.x_label)
    if request.y_label:
        plt.ylabel(request.y_label)
    if request.grid:
        plt.grid(request.grid)

    # 바 차트 그리기
    for i, y_data in enumerate(request.y_data):
        plt.bar(request.x_data, y_data, 
                color=request.bar_colors[i] if request.bar_colors else None,
                width=request.bar_widths[i] if request.bar_widths else None,
                label=request.legend_labels[i] if request.legend_labels else None)

    # 축 범위 설정
    if request.axis_range:
        plt.xlim(request.axis_range[0])
        plt.ylim(request.axis_range[1])

    # 범례 추가
    if request.legend_labels:
        plt.legend()

    plt.savefig(file_path)
    plt.close()

    # 생성된 이미지 파일의 URL 반환
    url = f"http://localhost:8989/{file_path}"


    # db에 저장   
    request_json = json.dumps(vars(request), indent=2)
    new_chart_history = ChartHistory(user_id= request.user_id, chart_type=request.chart_type,json=request_json, json_hash= request_hash, url=url )
    add_chart_history(new_chart_history)

    return {"url": url}
