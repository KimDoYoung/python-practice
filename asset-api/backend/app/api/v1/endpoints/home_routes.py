
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.app.core.template_engine import render_template
from backend.app.core.logger import get_logger
from backend.app.utils.misc_util import get_today

logger = get_logger()


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
    logger.debug(f">>> 페이지 요청받음: path:[{request.url.path}], client-IP: [{request.client.host}]")
    logger.debug(f"****************today_str in /main: {today_str}")
    context = { "request": request,  
                "page_path": '/main',
                "today": today_str}
        
    return render_template("main.html", context)

@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def page(
    request: Request, 
    path: str = Query(..., description="template폴더안의 html path")
):
    ''' path에 해당하는 페이지를 가져와서 쿼리 파라미터와 함께 렌더링한다.  '''
    logger.debug(f">>> 페이지 요청받음: path:[{request.url.path}], client-IP: [{request.client.host}]")
    
    today = get_today()
    # 추가적인 모든 쿼리 파라미터를 가져옴 (딕셔너리 형태로 변환)
    query_params = dict(request.query_params)

    # 'path'는 쿼리 파라미터에서 제외하고 context에 추가
    query_params.pop('path', None)    
    context = {
        "request": request, 
        "today" : today,
        "page_path": path, 
        **query_params  # 모든 추가적인 쿼리 파라미터를 context에 포함
    }
    # id = ipo_calendar 와 같은 형식이고 이를 분리한다.
    template_path = path.lstrip('/') 
    template_page = f"template/{template_path}.html"
    logger.debug(f"template_page 호출됨: {template_page}")
    return render_template(template_page, context)    

@router.get("/template", response_class=JSONResponse, include_in_schema=False)
async def handlebar_template(request: Request, path: str = Query(..., description="handlebar-template path")):
    ''' path에 해당하는 html에서 body추출해서 jinja2처리한 JSON을 리턴 '''
    
    logger.debug(f">>> 템플릿 요청받음: path:[{request.url.path}], client-IP: [{request.client.host}]")
    
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

