import json

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from logger import get_logger

from model.ChartRequest import BarChartRequest, ChartBase, LineChartRequest, PieChartRequest
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.charts_util import create_bar_chart, create_line_chart
from utils.db_utils import ChartHistory, Session, add_chart_history, calculate_request_hash, get_db
from typing import Dict


logger = get_logger(__name__)

router = APIRouter()

# 차트 타입에 따라 요청 클래스 매핑
chart_type_to_class = {
    "line": LineChartRequest,
    "bar": BarChartRequest,
    "pie": PieChartRequest,
}
# 챠트 그리를 함수들
chart_creator = {
    "line": create_line_chart,
    "bar": create_bar_chart
}

def get_chart_request(request: Dict) -> ChartBase:
    chart_type = request.get("chart_type")
    chart_class = chart_type_to_class.get(chart_type)
    if not chart_class:
        raise HTTPException(status_code=400, detail=f"Unsupported chart type: {chart_type}")
    try:
        return chart_class(**request)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error for {chart_type} chart: {e}")

@router.post("/chart")
async def chart_line(request: Dict = Body(...), db: Session = Depends(get_db)):

    # 차트 타입에 맞는 요청 객체로 변환
    chart_class = get_chart_request(request)
    chart_type = chart_class.chart_type
    
    # hash를 구해서 
    request_hash = calculate_request_hash(request)
    chart_history = db.query(ChartHistory).filter(ChartHistory.json_hash == request_hash).first()

    # 존재하면 url을 리턴
    if chart_history:
        logger.debug(f"already exists in chart_history table : {request_hash}")
        return JSONResponse(content={"url": chart_history.url})        
    

    #존재하지 않으면 chart생성
    try:
        chart_func = chart_creator[chart_type]
        url = chart_func(chart_class)
    except Exception as e:
        # 차트 생성 중 발생한 예외를 클라이언트에게 전달
        logger.error(f"ERROR:{str(e)}")
        raise HTTPException(status_code=400, detail={"error": str(e)})

    # db에 저장
    request_json = json.dumps(vars(chart_class), indent=2)
    new_chart_history = ChartHistory(user_id= chart_class.user_id, chart_type=chart_class.chart_type,json_data=request_json, json_hash= request_hash, url=url )
    add_chart_history(new_chart_history)

    return JSONResponse(content={"url": url})