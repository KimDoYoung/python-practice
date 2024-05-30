from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from backend.app.core.security import verify_token
from backend.app.core.config import config

STATIC_PATHS = ["/public", "/favicon.ico"]
async def jwt_auth_middleware(request: Request, call_next):
    
    # if request.url.path in ["/login", "/api/v1/users/login", "/calendar", "/main"] or any(request.url.path.startswith(path) for path in STATIC_PATHS):    
    if request.url.path in ["/login"] or any(request.url.path.startswith(path) for path in STATIC_PATHS):    
    # if request.url.path in ["/login", "/api/v1/users/login","/calendar","/main"]:
        response = await call_next(request)
        return response
        
    ACCESS_TOKEN_NAME = config.ACCESS_TOKEN_NAME
    token = request.cookies.get(ACCESS_TOKEN_NAME)
    try:
        if token:
            verify_token(token)
            response = await call_next(request)
        else:
            return RedirectResponse(url="/login")
    except HTTPException:
        return RedirectResponse(url="/login")
    return response
