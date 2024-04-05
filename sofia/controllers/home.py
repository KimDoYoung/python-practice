from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.template_engine import render_template

router = APIRouter()
# 메인 페이지 라우터
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request, "message": "Welcome to Sofia-주식매매시스템"}
    return render_template("index.html", context)