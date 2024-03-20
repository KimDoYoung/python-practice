from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from backend.app.api.endpoints.user import router as user_router

load_dotenv()  # 환경변수 로드

app = FastAPI()

app.include_router(user_router)

# "static" 폴더를 "/static" 경로에 마운트합니다.
# 이 예제에서는 프로젝트 루트 디렉토리에 "static" 폴더가 있고,
# 그 안에 "js", "css", "images" 등의 서브 디렉토리가 있다고 가정합니다.
# 현재 파일(main.py)의 위치를 기준으로 상대 경로를 구성합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_files_path = os.path.join(BASE_DIR, 'frontend', 'static')

app.mount("/static", StaticFiles(directory=static_files_path), name="static")

# 템플릿 환경 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, 'frontend/templates')),
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%', block_end_string='%)',
    variable_start_string='((', variable_end_string='))'
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    template = templates.get_template('pages/login.html')
    return HTMLResponse(template.render(request=request))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8686)), reload=True)
