from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

# 템플릿 인스턴스 생성
templates = Jinja2Templates(directory="templates")

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "입력 데이터가 유효하지 않습니다.", "details": exc.errors()},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    accept = request.headers.get("Accept")
    if "text/html" in accept:
        content = f"<html><body><h2>{exc.detail}</h2></body></html>"
        return HTMLResponse(content=content, status_code=exc.status_code)
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "서버 오류가 발생했습니다."}
    )

async def custom_404_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        accept = request.headers.get("Accept")
        if "text/html" in accept:
            return templates.TemplateResponse("common/error-404.html", {"request": request})
        else:
            return JSONResponse(
                status_code=404,
                content={"message": "Page not found"},
            )
    # For other HTTP errors, you can extend this handler by adding more conditions
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )