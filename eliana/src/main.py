from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import matplotlib
from exception.exception_handler import custom_404_exception_handler, general_exception_handler, http_exception_handler, validation_exception_handler

from utils.file_utils import get_file_path
matplotlib.use('Agg')  # GUI 백엔드를 'Agg'로 설정하여 GUI를 사용하지 않도록 함
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import base64
from io import BytesIO
from datetime import datetime
import os
import sys
from pathlib import Path
from routers import line, bar
from routers import form



src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.append(src_path)

app = FastAPI()

app.include_router(bar.router)
app.include_router(line.router)
app.include_router(form.router)

# charts 폴더를 정적 파일로 서빙하기 위해 애플리케이션에 마운트
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/charts", StaticFiles(directory="charts"), name="charts")

# exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_404_exception_handler)
# html template
templates = Jinja2Templates(directory="templates")

# fonts
# 현재 파일의 디렉토리 경로를 구함
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
font_path = os.path.join(parent_dir, 'assets', 'fonts', 'NanumGothic.ttf')
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'NanumGothic'

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # 템플릿 변수에 전달할 데이터
    data = {"title": "Creating charts via an API.", "description": "FastAPI with Jinja2 template."}
    # 템플릿 렌더링
    return templates.TemplateResponse("main.html", {"request": request, **data})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8989)
