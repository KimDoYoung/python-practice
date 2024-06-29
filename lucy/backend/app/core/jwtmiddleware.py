from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.core.security import verify_token


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 토큰이 필요 없는 URL 경로 정의
        STATIC_PATHS = ["/public", "/favicon.ico"]
        print(request.url.path)
        # if request.url.path in ["/login", "/logout", "/calendar", "/main"] or any(request.url.path.startswith(path) for path in STATIC_PATHS):    
        if request.url.path in ["/login", "/logout"] or any(request.url.path.startswith(path) for path in STATIC_PATHS):    
            response = await call_next(request)
            return response
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]

        if not auth_header:
            # URL 쿼리 파라미터에서 토큰 및 토큰 유형 추출
            token = request.cookies.get("lucy_token")

        try:
            if token:
                verify_token(token)
                # 쿠키를 제거하기 위해 Set-Cookie 헤더에 만료일을 과거로 설정
                #response.delete_cookie("token")
                response = await call_next(request)
                # response = Response(response.body, status_code=response.status_code, headers=dict(response.headers))
            else:
                return RedirectResponse(url="/login")
        except HTTPException:
            return RedirectResponse(url="/login")
        
        return response