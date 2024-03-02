from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates  # StaticFiles 임포트 추가
import uvicorn
import matplotlib

from utils.file_utils import get_file_path
matplotlib.use('Agg')  # GUI 백엔드를 'Agg'로 설정하여 GUI를 사용하지 않도록 함
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import base64
from io import BytesIO
from model import ChartRequest  # ChartRequest 클래스 임포트
from datetime import datetime
import os
import sys
from pathlib import Path


src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.append(src_path)

app = FastAPI()


# charts 폴더를 정적 파일로 서빙하기 위해 애플리케이션에 마운트
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/charts", StaticFiles(directory="charts"), name="charts")


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # 템플릿 변수에 전달할 데이터
    data = {"title": "Hello FastAPI", "description": "FastAPI with Jinja2 template."}
    # 템플릿 렌더링
    return templates.TemplateResponse("index.html", {"request": request, **data})

@app.post("/test")
def create_chart(request: ChartRequest):
    # 파일 경로 생성
    file_path = get_file_path(request.width, request.height)

    # 현재 파일의 디렉토리 경로를 구함
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)

    # fonts 폴더 내의 폰트 파일 경로를 구성
    font_path = os.path.join(current_dir, 'assets', 'fonts', 'NanumGothic.ttf')  # 'NanumGothic.ttf'를 예로 들었습니다.

    # 한글 폰트 설정
    # font_name = fm.FontProperties(fname=font_path).get_name()
    # plt.rc('font', family=font_name)
    # 폰트 매니저에 경로 추가
    fm.fontManager.addfont(font_path)

    # 폰트 설정
    plt.rcParams['font.family'] = 'NanumGothic'

    # 차트 생성 및 파일로 저장
    plt.figure(figsize=(request.width / 100, request.height / 100))
    plt.plot(request.x, request.y)
    plt.title("샘플챠트")
    plt.savefig(file_path)
    plt.close()

    # 생성된 이미지 파일의 URL 반환
    # 여기서는 예시로 localhost를 사용하고 있으나, 실제 배포 환경에 맞게 수정해야 합니다.
    url = f"http://localhost:8989/{file_path}"
    return {"url": url}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8989)
