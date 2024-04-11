from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.dependencies import get_db, get_folder_service
from core.template_engine import render_template

from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
# 메인 페이지 라우터
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db=Depends(get_db), folder_service = Depends(get_folder_service)):
    folder_list = await folder_service.get_all(db)
    folder_json_list = [folder.model_dump() for folder in folder_list]
    context = {"request": request, "message": "Welcome to Sofia-주식매매시스템", "list": folder_json_list}
    return render_template("index.html", context)