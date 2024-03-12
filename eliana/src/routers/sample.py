# Jinja2Templates 인스턴스 생성
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from logger_config import get_logger
from model.ChartRequest import ChartSampleRequest
from utils.db_utils import ChartSample, Session, get_db


# 이 파일의 디렉토리로부터 두 레벨을 올라가 프로젝트의 루트 디렉토리를 결정합니다
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))
#templates = Jinja2Templates(directory="../templates")

logger = get_logger(__name__)
router = APIRouter()
logger.debug(f"BASE_DIR : {BASE_DIR} ")
@router.get("/sample/insert/form", response_class=HTMLResponse)
async def sample_insert_form(request: Request):
    logger.debug("/sample/insert/form 호출됨...")
    html_file = f"sample/form.html"

    data = {"title": "Sample Json", "description": "FastAPI with Jinja2 template."}
    # 템플릿 렌더링
    html = templates.TemplateResponse(html_file, {"request": request, **data})
    logger.debug(html)
    return html #templates.TemplateResponse(html_file, {"request": request, **data})

# @router.post("/sample/insert", response_class=HTMLResponse)
# async def sample_insert(request: Request, chart_sample_data: ChartSampleRequest,  db: Session = Depends(get_db) ):
#     chart_sample = ChartSample(
#         chart_type=chart_sample_data.chart_type,
#         title=chart_sample_data.title,
#         json=chart_sample_data.data_json,
#         note=chart_sample_data.note
#     )
#     # db저장
#     db.add(chart_sample)
#     db.commit()
#     db.refresh(chart_sample)

#     html_file = f"sample/success.html"

#     # 성공 페이지 렌더링 준비
#     data = {
#         "request": request,  # HTTP 요청 정보
#         "title": "Sample Json",
#         "description": "FastAPI with Jinja2 template.",
#         "chart_sample": chart_sample  # 삽입된 차트 샘플 정보
#     }
#     # 템플릿 렌더링
#     return templates.TemplateResponse(html_file, data)

@router.post("/sample/insert", response_class=HTMLResponse)
async def sample_insert(request: Request, 
                        chart_type: str = Form(...),
                        title: str = Form(...),
                        json: str = Form(...),
                        note: str = Form(...),
                        db: Session = Depends(get_db) ):
    try:
        chart_sample_request = ChartSampleRequest(
            chart_type= chart_type,
            title=title,
            json=json,
            note=note
        )
    except ValidationError as e:
        # 유효성 검사 실패 시 오류 반환
                # ValidationError 예외에서 상세한 오류 정보 추출
        details = e.errors()
        # HTTPException에 오류 정보 전달
        raise HTTPException(status_code=400, detail={"errors": details})
    
        # SQLAlchemy 모델 인스턴스 생성
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

    html_file = f"common/success.html"

    # 성공 페이지 렌더링 준비
    data = {
        "request": request,  # HTTP 요청 정보
        "title": "Sample Json",
        "description": "FastAPI with Jinja2 template.",
        "chart_sample": chart_sample  # 삽입된 차트 샘플 정보
    }
    # 템플릿 렌더링
    return templates.TemplateResponse(html_file, data)