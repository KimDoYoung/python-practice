import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import  JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape

from logger import get_logger
from utils.db_utils import  get_chart_samples_by_type, get_db
from utils.eliana_util import chartTypeName
from sqlalchemy.orm import Session

# 이 파일의 디렉토리로부터 두 레벨을 올라가 프로젝트의 루트 디렉토리를 결정합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')), 
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%', block_end_string='%)',
    variable_start_string='((', variable_end_string='))',    
)


logger = get_logger(__name__)
router = APIRouter()

@router.get("/form/{chart_type}", response_class=JSONResponse)
async def form_chart(request: Request, chart_type: str,  db: Session = Depends(get_db)):

    # html_file = f"form/{chart_type}.html"
    html_file = f"form/chart-main.html"
    samples = get_chart_samples_by_type(chart_type, db)
    logger.debug("sample size: " + str( len(samples)))
    # 템플릿 렌더링을 위한 데이터
    chartName = chartTypeName(chart_type)
    data = {"samples": samples, "chartType" : chart_type, "chartName" : chartName}
    
    # 템플릿 불러오기 및 렌더링
    template = env.get_template(html_file)
    html_content = template.render(request=request, **data)


    # handlebar 템플릿과 데이터를 반환
    return JSONResponse(content={"template": html_content })
