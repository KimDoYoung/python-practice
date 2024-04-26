import os
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.app.core.logger import get_logger
from backend.app.core.template_engine import render_template
from backend.app.core.configs import PROFILE_NAME

logger = get_logger(__name__)

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
        return render_template("common/error.html", {"message": exc.detail, "status_code": exc.status_code}, exc.status_code)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """일반 예외 처리"""
    if PROFILE_NAME == "local":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={ "message" : f"서버 오류가 발생했습니다. {str(exc)}" }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "서버 오류가 발생했습니다."}
        )

async def custom_404_exception_handler(request: Request, exc: StarletteHTTPException) -> HTMLResponse:
    """404 예외 처리"""
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        accept = request.headers.get("Accept")
        if "text/html" in accept:
            # 404 에러 페이지 템플릿 렌더링
            return render_template("common/error-404.html", {"request": request}, exc.status_code)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "요청하신 페이지를 찾을 수 없습니다."},
            )
    # 다른 HTTP 예외에 대한 기본 처리
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
