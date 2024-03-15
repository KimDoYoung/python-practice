import json
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from logger import get_logger

from model.ChartRequest import LineChartRequest
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.charts_util import create_line_chart
from utils.db_utils import ChartHistory, Session, add_chart_history, calculate_request_hash, get_db
from utils.file_utils import get_file_path

logger = get_logger(__name__)

router = APIRouter()

@router.post("/chart/line")
async def chart_line(request: LineChartRequest, db: Session = Depends(get_db)):

    logger.debug(f"/chart/line start : {request}")
    # hash를 구해서 
    request_hash = calculate_request_hash(request);
    chart_history = db.query(ChartHistory).filter(ChartHistory.json_hash == request_hash).first()

    # 존재하면 url을 리턴
    if chart_history:
        logger.debug(f"already exists in chart_history table : {request_hash}")
        return JSONResponse(content={"url": chart_history.url})        
    
    #존재하지 않으면 chart생성
    try:
        url = create_line_chart(request)
    except Exception as e:
        # 차트 생성 중 발생한 예외를 클라이언트에게 전달
        logger.error(f"ERROR:{str(e)}")
        raise HTTPException(status_code=400, detail={"error": str(e)})

    # db에 저장
    request_json = json.dumps(vars(request), indent=2)
    new_chart_history = ChartHistory(user_id= request.user_id, chart_type=request.chart_type,json_data=request_json, json_hash= request_hash, url=url )
    add_chart_history(new_chart_history)

    return JSONResponse(content={"url": url})