# Jinja2Templates 인스턴스 생성
import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape

from logger_config import get_logger
from utils.db_utils import Session, get_chart_samples_by_type, get_db


# templates = Jinja2Templates(directory="../templates")

# 이 파일의 디렉토리로부터 두 레벨을 올라가 프로젝트의 루트 디렉토리를 결정합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')), autoescape=select_autoescape(['html', 'xml']))


logger = get_logger(__name__)
router = APIRouter()

@router.get("/form/{chart_type}", response_class=JSONResponse)
async def form_chart(request: Request, chart_type: str,  db: Session = Depends(get_db)):

    html_file = f"form/{chart_type}.html"
    samples = get_chart_samples_by_type(db, chart_type);
    logger.debug("sample size: " + str( len(samples)))
    # 템플릿 렌더링을 위한 데이터
    data = {"samples": samples}
    
    # 템플릿 불러오기 및 렌더링
    template = env.get_template(html_file)
    html_content = template.render(request=request, **data)


    # handlebar 템플릿과 데이터를 반환
    return JSONResponse(content={"template": html_content })
