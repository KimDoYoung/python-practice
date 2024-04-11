from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.template_engine import render_template
from core.dependencies import folder_service_dependency, db_dependency
import json

from core.util import datetime_serializer

from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()
# 메인 페이지 라우터
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: db_dependency, folder_service : folder_service_dependency):
    # TODO 현재 folder 목록을 가져온다.
    folder_list = await folder_service.get_all(db)
    # Convert List[ImageFolders] to JSON object list
    folder_json_list = [folder.model_dump() for folder in folder_list]
    #list = json.dumps(folder_json_list, default=datetime_serializer, indent=4)
    #logger.debug(f"folder_list: {list}")
    context = {"request": request, "message": "Welcome to Sofia-주식매매시스템", "list": folder_json_list}
    return render_template("index.html", context)