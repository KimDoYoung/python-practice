
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.app.core.template_engine import get_template_html, render_template


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
    # id = ipo_calendar 와 같은 형식이고 이를 분리한다.
    #path_array = id.split("_")
    template_path = path
    template_page = f"templates/{template_path}.html"
    logger.debug(f"template_page 호출됨: {template_page}")

    return render_template(template_page, context)    

@router.get("/template", response_class=JSONResponse, include_in_schema=False)
async def handlebar_template(request: Request, path: str = Query(..., description="handlebar-template path")):

    handlebar_template = get_template_html(path)
    data = {
        "template": handlebar_template
    }
    return JSONResponse(content=data)