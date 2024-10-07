
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.app.core.template_engine import render_template
from backend.app.core.settings import config
from backend.app.core.logger import get_logger
from backend.app.utils.misc_util import get_today

logger = get_logger(__name__)


router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def display_root(request: Request):
    ''' 메인 '''
    return RedirectResponse(url="/main")


@router.get("/main", response_class=HTMLResponse, include_in_schema=False)
async def display_main(request: Request):
    ''' 메인 '''    
    logger.debug("***************Calling get_today() function for /main endpoint")
    today_str = get_today()
    logger.debug(f"****************today_str in /main: {today_str}")
    context = { "request": request,  
                "page_path": '/main',
                "today": today_str}
        
    return render_template("main.html", context)

@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def page(
    request: Request, 
    path: str = Query(..., description="template폴더안의 html path"),
    stk_code: str = Query(None, description="선택적 주식 코드")
):
    ''' path에 해당하는 페이지를 가져와서 보낸다. '''
    
    # 쿠키에서 stk_code를 가져오거나, 쿼리 파라미터로 전달된 stk_code를 사용
    cookie_stk_code = request.cookies.get("stk_code")
    stk_code = stk_code or cookie_stk_code    

    today = get_today()
    context = {
        "request": request, 
        "today" : today,
        "page_path": path, 
    }
    # id = ipo_calendar 와 같은 형식이고 이를 분리한다.
    template_path = path.lstrip('/') 
    template_page = f"template/{template_path}.html"
    logger.debug(f"template_page 호출됨: {template_page}")
    return render_template(template_page, context)    

@router.get("/template", response_class=JSONResponse, include_in_schema=False)
async def handlebar_template(request: Request, path: str = Query(..., description="handlebar-template path")):
    ''' path에 해당하는 html에서 body추출해서 jinja2처리한 JSON을 리턴 '''
    today = get_today()
    context = {
        "request": request, 
        "today" : today
    }
    # '/'로 시작하면 '/' 제거
    if path.startswith('/'):
        path = path.lstrip('/')
    
    # ".html"로 끝나면 ".html" 제거
    path = path.removesuffix('.html')
    
    handlebar_html_filename =  f"handlebar/{path}.html"

    handlebar_html =  render_template(handlebar_html_filename, context)
    data = {
        "template": handlebar_html
    }
    return JSONResponse(content=data)

