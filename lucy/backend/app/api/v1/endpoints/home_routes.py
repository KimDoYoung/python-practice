
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.app.core.template_engine import render_template
from backend.app.core.config import config
from backend.app.core.security import create_access_token, get_current_user
from fastapi import status

from backend.app.domains.user.user_model import AccessToken, LoginFormData
from backend.app.domains.user.user_service import UserService
from backend.app.core.dependency import get_user_service
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
    
    logger.debug("***************Calling get_today() function for /main endpoint")
    today_str = get_today()
    logger.debug(f"****************today_str in /main: {today_str}")
    stk_code = request.cookies.get("stk_code")
    context = { "request": request,  
                "user_id":  current_user["user_id"], 
                "user_name": current_user["user_name"], 
                "today": today_str,
                "stk_code": stk_code}    
    return render_template("main.html", context)

@router.get("/page", response_class=HTMLResponse, include_in_schema=False)
async def page(request: Request, path: str = Query(..., description="template폴더안의 html path")):
    ''' path에 해당하는 페이지를 가져와서 보낸다. '''
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

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    ''' 로그인 페이지 '''
    return render_template("login.html", {"request": request})

@router.get("/logout", response_class=JSONResponse)
async def logout(response: Response):
    ''' 로그아웃 페이지 '''
    response.delete_cookie(config.ACCESS_TOKEN_NAME)
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return response

@router.post("/login", response_model=AccessToken)
async def login_for_access_token(form_data: LoginFormData, user_service :UserService=Depends(get_user_service)):
    ''' 로그인 프로세스'''
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    user_id = user.user_id
    user_name = user.user_name
    access_token = create_access_token(
        data={"user_id": user_id, "name": user_name}, expires_delta=access_token_expires
    )
    access_token = AccessToken(access_token=access_token, token_type="bearer",username=user_name, email=user.email) 
    return access_token
