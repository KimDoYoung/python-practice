
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.app.core.template_engine import render_template


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

    today_str = get_today()
    context = { "request": request,  
                "today": today_str}    
    return render_template("main.html", context)

@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def page(request: Request, path: str = Query(..., description="template path")):
    ''' id 페이지를 가져와서 보낸다. '''
    
    today = get_today()
    context = {
        "request": request, 
        "today" : today,
        "page-id": id, 
    }
    template_path = path
    template_page = f"templates/{template_path}.html"
    logger.debug(f"template_page 호출됨: {template_page}")

    return render_template(template_page, context)    

@router.get("/template", response_class=JSONResponse, include_in_schema=False)
async def handlebar_template(request: Request, path: str = Query(..., description="handlebar-template path")):
    ''' path에 해당하는 html에서 body추출해서 jinja2처리한 html을 반환한다. '''
    today = get_today()
    context = {
        "request": request, 
        "today" : today
    }
    handlebar_html =  f"handlebar/{path}"
    handlebar_html =  render_template(handlebar_html, context)    
    data = {
        "template": handlebar_html
    }
    return JSONResponse(content=data)