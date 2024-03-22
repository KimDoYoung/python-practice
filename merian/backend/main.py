from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from backend.app.api.endpoints.user import router as user_router
from backend.app.api.endpoints.keyboard import router as keyboqrd_router

load_dotenv()  # 환경변수 로드

app = FastAPI()

app.include_router(user_router)
app.include_router(keyboqrd_router)

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

def extract_body_content(html_content):
    start = html_content.find('<body>')
    end = html_content.find('</body>')
    if start != -1 and end != -1:
        return html_content[start+len('<body>'):end].strip()
    return ""

# HTML 파일을 읽고 내용을 추출하는 예시
def read_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        body_content = extract_body_content(html_content)
        return body_content

def render_html_template(template_name: str, context: dict = None, request: Request = None) -> HTMLResponse:
    context = context or {}
    template = templates.get_template(template_name)
    content = template.render(request=request, **context)
    return HTMLResponse(content)
    
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    template = templates.get_template('pages/login.html')
    return HTMLResponse(template.render(request=request))
    
@app.get("/main", response_class=HTMLResponse)
async def read_root(request: Request, pageId: str = Query(default="keyboard-list")):
    keyboard_list = read_html_content('frontend/templates/pages/keyboard/list.html')
    keyboard_insert = read_html_content('frontend/templates/pages/keyboard/insert.html')
    keyboard_edit = read_html_content('frontend/templates/pages/keyboard/edit.html')

    context = {
        "pageId": pageId,
        "keyboard_list": keyboard_list,
        "keyboard_insert": keyboard_insert,
        "keyboard_edit": keyboard_edit
    }

    return render_html_template('pages/main.html', context=context, request=request)    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8686)), reload=True)
