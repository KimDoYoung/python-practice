
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from backend.app.core.template_engine import render_template
from backend.app.core.config import config
from backend.app.core.security import create_access_token
from fastapi import status

from backend.app.domains.user.user_model import AccessToken, LoginFormData
from backend.app.domains.user.user_service import UserService
from backend.app.core.dependency import get_user_service

router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def display_main(request: Request):
    ''' 메인 '''
    context = {"request": request, "message": "Welcome to Joanna API!-주식(공모주) 자동 매매시스템"}
    return render_template("main.html", context)

@router.get("/main", response_class=HTMLResponse, include_in_schema=False)
def display_main(request: Request):
    ''' 메인 '''
    context = {}

    return render_template("main.html", context)

@router.get("/ipo/calendar", response_class=HTMLResponse, include_in_schema=False)
def display_main(request: Request):
    ''' 달력-스케줄 '''
    context = {}
    return render_template("template/ipo/calendar.html", context)

@router.get("/ipo", response_class=HTMLResponse, include_in_schema=False)
def display_main(request: Request):
    ''' ipo list '''
    context = {}
    return render_template("template/ipo/list.html", context)


@router.get("/scheduler", response_class=HTMLResponse, include_in_schema=False)
def display_main(request: Request):
    ''' ipo list '''
    context = {}
    return render_template("template/scheduler/list.html", context)


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
