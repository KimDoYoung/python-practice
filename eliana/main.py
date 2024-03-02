from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles  # StaticFiles 임포트 추가
import uvicorn
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from ChartRequest import ChartRequest  # ChartRequest 클래스 임포트
from datetime import datetime
import os

def get_file_path(width: int, height: int, base_dir="static") -> str:
    """
    차트 이미지를 저장할 파일 경로를 생성하는 함수.
    
    :param width: 이미지의 너비
    :param height: 이미지의 높이
    :param base_dir: 기본 디렉토리 경로
    :return: 생성된 파일 경로
    """
    current_date = datetime.now()
    date_path = current_date.strftime("%Y/%m")
    directory_path = f"{base_dir}/{date_path}"

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # 파일 이름에 현재 날짜와 시간을 포함
    file_name = f"chart_{width}x{height}_{current_date.strftime('%Y%m%d%H%M%S')}.png"
    return f"{directory_path}/{file_name}"

app = FastAPI()

# static 폴더를 정적 파일로 서빙하기 위해 애플리케이션에 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/test")
def create_chart(request: ChartRequest):
    # 파일 경로 생성
    file_path = get_file_path(request.width, request.height)

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
