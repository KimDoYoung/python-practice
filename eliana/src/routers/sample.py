# Jinja2Templates 인스턴스 생성
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import ValidationError

from logger_config import get_logger
from model.ChartRequest import ChartSampleRequest
from utils.db_utils import ChartSample, Session, get_db


# 이 파일의 디렉토리로부터 두 레벨을 올라가 프로젝트의 루트 디렉토리를 결정합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')), autoescape=select_autoescape(['html', 'xml']))

logger = get_logger(__name__)
router = APIRouter()
logger.debug(f"BASE_DIR : {BASE_DIR} ")

@router.get("/sample/insert/form", response_class=JSONResponse)
async def sample_insert_form(request: Request, db: Session = Depends(get_db) ):
    logger.debug("/sample/insert/form 호출됨...")
    chart_sample_list = db.query(ChartSample).all()

    html_file = "sample/sample-form.html"

    # 템플릿 렌더링을 위한 데이터
    data = {"title": "Sample Json", "description": "FastAPI with Jinja2 template."}
    
    # 템플릿 불러오기 및 렌더링
    template = env.get_template(html_file)
    html_content = template.render(request=request, **data)
    
    logger.debug(html_content)
    
    # HTML 내용을 JSON 응답의 일부로 반환
    return JSONResponse(content={"template": html_content})



@router.post("/sample/insert", response_class=JSONResponse)
async def sample_insert(request: Request, chart_sample_request: ChartSampleRequest, db: Session = Depends(get_db) ):

    chart_sample = ChartSample(
        chart_type=chart_sample_request.chart_type,
        title=chart_sample_request.title,
        json=chart_sample_request.json,  # 'json' 필드에 'data_json' 값을 할당
        note=chart_sample_request.note
    )

    # db저장
    db.add(chart_sample)
    db.commit()
    db.refresh(chart_sample)

    # 템플릿 렌더링
    return {"result" : "OK"}


@router.delete("/sample/delete/{id}", response_class=JSONResponse)
async def delete_chart_sample(id: int, db: Session = Depends(get_db)):
    # ID를 사용하여 ChartSample 레코드 조회
    chart_sample = db.query(ChartSample).filter(ChartSample.id == id).first()
    if chart_sample is None:
        raise HTTPException(status_code=404, detail="ChartSample not found")

    # 레코드 삭제
    db.delete(chart_sample)
    db.commit()

    return {"result": "OK"}