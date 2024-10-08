# exception_handler.py
"""
모듈 설명: 
    - exception_handler.py는 FastAPI 앱의 예외 처리를 담당하는 모듈입니다.
에러 메시지:

    
작성자: 김도영
작성일: 03
버전: 1.0
"""
from datetime import datetime
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
from jinja2 import TemplateNotFound

from backend.app.core.logger import get_logger
from backend.app.core.template_engine import render_template

logger = get_logger(__name__)

def add_exception_handlers(app):
    """FastAPI 앱에 예외 핸들러를 등록하는 함수"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    app.add_exception_handler(StarletteHTTPException, custom_404_exception_handler)

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Union[JSONResponse, HTMLResponse]:
    """입력 데이터 유효성 검사 예외 처리"""
    return await create_error_response(request, exc, exc.errors())

async def http_exception_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, HTMLResponse]:
    """HTTP 예외 처리"""
    return await create_error_response(request, exc)

async def general_exception_handler(request: Request, exc: Exception) -> Union[JSONResponse, HTMLResponse]:
    """일반 예외 처리"""
    if isinstance(exc, TemplateNotFound):
        logger.error(f"템플릿을 찾을 수 없습니다: {exc}")
        # 템플릿을 찾지 못했을 때 기본 HTML 페이지를 반환
        context = {
            "request": request.url.path,
            "status_code": 500,
            "detail": "템플릿을 찾을 수 없습니다.",
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # return HTMLResponse(
        #     content="<h1>500 - Internal Server Error</h1><p>템플릿을 찾을 수 없습니다.</p>",
        #     status_code=500
        # )    
        return HTMLResponse(content=render_template("error.html", context), status_code=context["status_code"])
    return await create_error_response(request, exc)

# 유효성 검사 에러 처리 핸들러 (Pydantic validation error)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """유효성 검사 실패 예외 처리"""
    server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.error(f"유효성 검사 에러: {exc.errors()}")

    context = {
        "request": request.url.path,
        "status_code": 422,
        "detail": str(exc), #exc.errors(),
        "server_time": server_time  # 항상 server_time을 추가
    }

    return JSONResponse(status_code=422, content=context)

async def custom_404_exception_handler(request: Request, exc: StarletteHTTPException) -> Union[JSONResponse, HTMLResponse]:
    """404 예외 처리"""
    return await create_error_response(request, exc)

async def create_error_response(request: Request, exc: Exception, errors=None) -> Union[JSONResponse, HTMLResponse]:
    """에러 응답 생성 함수"""
    logger.error(f"xxx [500] xxx --> 서버동작 중 오류 발생: {exc}")
    context = {
        "request": request.url.path,
        "status_code": getattr(exc, "status_code", 500),
        "detail": getattr(exc, "detail", "Internal Server Error :" + str(exc)),
        "errors": errors or [],
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    accept = request.headers.get("Accept", "")
    if "text/html" in accept:
        return HTMLResponse(content=render_template("error.html", context), status_code=context["status_code"])
    else:
        return JSONResponse(
            status_code=context["status_code"],
            content=context,
        )

