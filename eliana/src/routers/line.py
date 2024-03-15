import json
import os
from fastapi import APIRouter, Depends
from logger import get_logger

from model.ChartRequest import LineChartRequest
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.db_utils import ChartHistory, Session, add_chart_history, calculate_request_hash, get_db
from utils.file_utils import get_file_path

logger = get_logger(__name__)

router = APIRouter()

@router.post("/chart/line")
async def chart_line(request: LineChartRequest, db: Session = Depends(get_db)):

    logger.debug(request)
    title = request.title
    # hash를 구해서 
    request_hash = calculate_request_hash(request);
    chart_history = db.query(ChartHistory).filter(ChartHistory.json_hash == request_hash).first()

    # 존재하면 url을 리턴
    if chart_history:
        return {"url": chart_history.url}

    # 파일 경로 얻기
    file_path = get_file_path(request.width, request.height)

    # 차트 생성 로직 (예: matplotlib 사용)
    plt.figure(figsize=(request.width / 100, request.height / 100))

    if request.title:
        plt.title(request.title)
    if request.x_label:
        plt.xlabel(request.x_label)
    if request.y_label:
        plt.ylabel(request.y_label)
    if request.grid:
        plt.grid(request.grid)

    # 라인 그리기
    for i, y_data in enumerate(request.y_data):
        plt.plot(request.x_data, y_data,
                color=request.line_colors[i] if request.line_colors else None,
                linestyle=request.line_styles[i] if request.line_styles else None,
                linewidth=request.line_widths[i] if request.line_widths else None,
                marker=request.marker_styles[i] if request.marker_styles else None,
                label=request.legend_labels[i] if request.legend_labels else None)

        # 텍스트 라벨 추가
        if request.text_labels:
            for text_label in request.text_labels[i]:
                plt.text(text_label[0], text_label[1], text_label[2])

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
    new_chart_history = ChartHistory(user_id= request.user_id, chart_type=request.chart_type,json_data=request_json, json_hash= request_hash, url=url )
    add_chart_history(new_chart_history)

    return {"url": url, "title": title }