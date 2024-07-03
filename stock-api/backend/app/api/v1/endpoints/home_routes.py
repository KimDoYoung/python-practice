
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from backend.app.core.template_engine import render_template
from backend.app.core.security import get_current_user

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
    current_user = await get_current_user(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token-현재 사용자 정보가 없습니다")
    
    today_str = get_today()
    stk_code = request.cookies.get("stk_code")
    context = { "request": request,  
                "user_id":  current_user["user_id"], 
                "user_name": current_user["user_name"], 
                "today": today_str,
                "stk_code": stk_code}    
    return render_template("main.html", context)

@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def page(request: Request, id: str = Query(..., description="The ID of the page")):
    ''' id 페이지를 가져와서 보낸다. '''
    current_user = await get_current_user(request)
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid token-현재 사용자 정보가 없습니다")
    stk_code = request.cookies.get("stk_code")
    today = get_today()
    context = {
        "request": request, 
        "today" : today,
        "page-id": id, 
        "user_id": current_user["user_id"], 
        "user_name": current_user["user_name"],
        "stk_code" : stk_code
    }
    # id = ipo_calendar 와 같은 형식이고 이를 분리한다.
    path_array = id.split("_")
    template_path = "/".join(path_array)
    template_page = f"template/{template_path}.html"
    logger.debug(f"template_page 호출됨: {template_page}")

    return render_template(template_page, context)    

