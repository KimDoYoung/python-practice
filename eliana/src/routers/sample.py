# Jinja2Templates 인스턴스 생성
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import ValidationError

from logger import get_logger
from model.ChartRequest import ChartSampleRequest
from utils.db_utils import ChartSample, Session, get_db
from utils.eliana_util import chartTypeName


# 이 파일의 디렉토리로부터 두 레벨을 올라가 프로젝트의 루트 디렉토리를 결정합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%', block_end_string='%)',
    variable_start_string='((', variable_end_string='))'
)

logger = get_logger(__name__)
router = APIRouter()

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
    
    #logger.debug(html_content)
    
    # HTML 내용을 JSON 응답의 일부로 반환
    return JSONResponse(content={"template": html_content})



@router.post("/sample/insert", response_class=JSONResponse)
async def sample_insert(request: Request, chart_sample_request: ChartSampleRequest, db: Session = Depends(get_db) ):

    chart_sample = ChartSample(
        chart_type=chart_sample_request.chart_type,
        title=chart_sample_request.title,
        json_data=chart_sample_request.json_data,  # 'json' 필드에 'data_json' 값을 할당
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

#샘플 수정 폼 표시
@router.get("/sample/edit/form/{id}", response_class=JSONResponse)
async def sample_edit_form(id:int, db: Session = Depends(get_db) ):
    logger.debug("/sample/edit/form 호출됨...")
     # id를 기준으로 chart_sample 테이블에서 데이터 조회
    sample = db.query(ChartSample).filter(ChartSample.id == id).first()
    
    # 조회된 데이터가 없다면 404 에러 반환
    if sample is None:
        raise HTTPException(status_code=404, detail="Item not found")

    html_file = "sample/sample-form-edit.html"

    # 템플릿 렌더링을 위한 데이터
    data = {"sample" : sample, "chartTypeName": chartTypeName(sample.chart_type)}
    
    # 템플릿 불러오기 및 렌더링
    template = env.get_template(html_file)
    html_content = template.render(**data)
    
    logger.debug(html_content)
    
    # HTML 내용을 JSON 응답의 일부로 반환
    return JSONResponse(content={"template": html_content})

@router.post("/sample/edit/{id}", response_class=JSONResponse)
async def sample_edit(id:int, request: Request, chart_sample_request: ChartSampleRequest, db: Session = Depends(get_db) ):

    # chart_sample_request에서 id를 이용하여 DB에서 해당 레코드 조회
    chart_sample = db.query(ChartSample).filter(ChartSample.id == id).first()
    
    if chart_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")

    # 조회된 인스턴스의 속성을 업데이트
    chart_sample.chart_type = chart_sample_request.chart_type
    chart_sample.title = chart_sample_request.title
    chart_sample.json_data = chart_sample_request.json_data  # 'json' 필드에 'data_json' 값을 할당하려면, 해당 스키마에서 이 필드를 처리하는 방식을 확인해야 합니다.
    chart_sample.note = chart_sample_request.note

    # 데이터베이스에 변경 사항을 커밋
    db.commit()

    # 변경된 인스턴스를 다시 로드하여 최신 상태 반영
    db.refresh(chart_sample)

    # 응답 반환
    return {"result": "OK"}

# 샘플선택이 되었을 때 1개를 찾아서 가져온 후 json데이터를 보내준다.
@router.get("/sample/{id}", response_class=JSONResponse)
async def delete_chart_sample(id: int, db: Session = Depends(get_db)):
    # ID를 사용하여 ChartSample 레코드 조회
    chart_sample = db.query(ChartSample).filter(ChartSample.id == id).first()
    if chart_sample is None:
        raise HTTPException(status_code=404, detail="ChartSample not found")
    jsonData = chart_sample.json_data;
    return JSONResponse(content={"jsonData": jsonData})
