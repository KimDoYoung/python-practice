import os
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.exceptions import HTTPException as StarletteHTTPException


# 프로젝트 루트 디렉토리를 기반으로 템플릿 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_dir = os.path.join(BASE_DIR, 'templates')

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%', block_end_string='%)',
    variable_start_string='((', variable_end_string='))'
)

def render_html_response(template_name: str, context: dict, status_code: int) -> HTMLResponse:
    """HTML 응답을 생성하는 함수"""
    template = env.get_template(template_name)
    html_content = template.render(**context)
    return HTMLResponse(content=html_content, status_code=status_code)

def add_exception_handlers(app):
    """FastAPI 앱에 예외 핸들러를 등록하는 함수"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    app.add_exception_handler(StarletteHTTPException, custom_404_exception_handler)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """입력 데이터 유효성 검사 예외 처리"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "입력 데이터가 유효하지 않습니다.", "details": exc.errors()},
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP 예외 처리"""
    accept = request.headers.get("Accept")
    if "text/html" in accept:
        # HTML 응답을 위한 기본 에러 템플릿 사용
        return render_html_response("common/error.html", {"message": exc.detail, "status_code": exc.status_code}, exc.status_code)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """일반 예외 처리"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "서버 오류가 발생했습니다.", "details": str(exc)}
    )

async def custom_404_exception_handler(request: Request, exc: StarletteHTTPException) -> HTMLResponse:
    """404 예외 처리"""
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        accept = request.headers.get("Accept")
        if "text/html" in accept:
            # 404 에러 페이지 템플릿 렌더링
            return render_html_response("common/error-404.html", {"request": request}, exc.status_code)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Page not found"},
            )
    # 다른 HTTP 예외에 대한 기본 처리
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
