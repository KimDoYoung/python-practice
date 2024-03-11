# Jinja2Templates 인스턴스 생성
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from logger_config import get_logger


templates = Jinja2Templates(directory="../templates")

logger = get_logger(__name__)
router = APIRouter()

@router.get("/form/{chart_type}", response_class=JSONResponse)
async def form_chart(request: Request, chart_type: str):

    chartTypeNames = {'line' : '라인 챠트', 'bar' : '막대 챠트' }
    # HTML 파일 열기 및 읽기
    html_file = f"templates/form/{chart_type}.html"
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # <body> 태그 사이의 내용 추출
    start = html_content.find('<body>') + len('<body>')
    end = html_content.find('</body>')
    body_content = html_content[start:end].strip()

    # handlebar 템플릿과 데이터를 반환
    return JSONResponse(content={"template": body_content, "data": {"chartTypeName" : chartTypeNames[chart_type]} })
