from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import matplotlib
from exception.exception_handler import custom_404_exception_handler, general_exception_handler, http_exception_handler, validation_exception_handler
from utils.db_utils import ChartSample, Session, get_db

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
from routers import chart
from routers import form, sample

src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.append(src_path)

app = FastAPI()

# app.include_router(bar.router)
# app.include_router(line.router)
app.include_router(chart.router)
app.include_router(form.router)
app.include_router(sample.router)

# charts 폴더를 정적 파일로 서빙하기 위해 애플리케이션에 마운트
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/charts", StaticFiles(directory="charts"), name="charts")

# exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_404_exception_handler)

# fonts
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
font_path = os.path.join(parent_dir, 'assets', 'fonts', 'NanumGothic.ttf')
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'NanumGothic'


# Jinja2 환경 설정
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%', block_end_string='%)',
    variable_start_string='((', variable_end_string='))'
)

@app.get("/", response_class=HTMLResponse)
def root_page(request: Request):
    # 템플릿 변수에 전달할 데이터
    data = {"title": "Creating charts via an API.", "description": "FastAPI with Jinja2 template."}
    # 템플릿 렌더링
    template = env.get_template('main.html')
    html_content = template.render(data)
    return html_content

@app.get("/chart", response_class=JSONResponse)
def chart_page(request: Request):
    
    # 템플릿 데이터
    data = {"title": "Chart", "description": "This is a chart rendered by Jinja2."}
    
    # 템플릿 불러오기 및 렌더링
    template = env.get_template('form/chart.html')
    html_content = template.render(data)
    
    # 렌더링된 HTML 내용을 JSONResponse의 일부로 반환
    return JSONResponse(content={"template": html_content})

@app.get("/sample", response_class=JSONResponse)
def chart_page(request: Request, db: Session = Depends(get_db)):
    chart_samples = db.query(ChartSample).order_by(ChartSample.created_on.desc()).limit(20).all()
    # 템플릿 불러오기 및 렌더링
    template = env.get_template('sample/sample-list.html')
    html_content = template.render(request=request, chart_samples=chart_samples)
   
    # 렌더링된 HTML 내용을 JSONResponse의 일부로 반환
    return JSONResponse(content={"template": html_content})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8989)
