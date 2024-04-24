from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from backend.app.core.template_engine import render_template


router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def display_index(request: Request):
    ''' 메인 '''
    context = {"request": request, "message": "Welcome to Joanna API!-주식매매시스템"}
    return render_template("index.html", context)

@router.get("/stockapi", response_class=HTMLResponse, include_in_schema=False)
def display_index(request: Request):
    ''' 증권사 메인 '''
    context = {"request": request, "message": "Welcome to Joanna API!-주식매매시스템"}
    return render_template("stockapi/index.html", context)

@router.get("/openapi", response_class=HTMLResponse, include_in_schema=False)
def display_index(request: Request):
    ''' Open api 메인 '''
    context = {"request": request, "message": "Welcome to Joanna API!-주식매매시스템"}
    return render_template("openapi/index.html", context)
