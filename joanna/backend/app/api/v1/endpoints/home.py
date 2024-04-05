from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from backend.app.core.template_engine import render_template


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def display_index(request: Request):
    context = {"request": request, "message": "Welcome to Joanna API!-주식매매시스템"}
    return render_template("index.html", context)
