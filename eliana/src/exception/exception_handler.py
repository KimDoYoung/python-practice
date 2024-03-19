import os
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.exceptions import HTTPException as StarletteHTTPException

# 템플릿 인스턴스 생성
# 이 파일의 디렉토리로부터 두 레벨을 올라가 프로젝트의 루트 디렉토리를 결정합니다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%', block_end_string='%)',
    variable_start_string='((', variable_end_string='))'
)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "입력 데이터가 유효하지 않습니다.", "details": exc.errors()},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    accept = request.headers.get("Accept")
    if "text/html" in accept:
        return HTMLResponse(content=content, status_code=exc.status_code)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "서버 오류가 발생했습니다.","details": str(exc)}
    )

async def custom_404_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        accept = request.headers.get("Accept")
        if "text/html" in accept:
            template = env.get_template("common/error-404.html")
            html = template.render(request=request)
            return HTMLResponse(content=html, status_code=exc.status_code)
        else:
            return JSONResponse(
                status_code=404,
                content={"message": "Page not found"},
            )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )