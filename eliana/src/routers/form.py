# Jinja2Templates 인스턴스 생성
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="../templates")

router = APIRouter()

@router.get("/form/linebar", response_class=JSONResponse)
async def get_form_linebar(request: Request):

    # HTML 파일 열기 및 읽기
    with open('templates/form/linebar.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # <body> 태그 사이의 내용 추출
    start = html_content.find('<body>') + len('<body>')
    end = html_content.find('</body>')
    body_content = html_content[start:end].strip()
    # handlebar 템플릿과 데이터를 반환
    return JSONResponse(content={"template": body_content, "data": {"chartTypeName" : "라인/바 챠트"} })
    #return templates.TemplateResponse(body_content, {"request": request, "data": data})
