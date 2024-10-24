import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.logger import get_logger
from backend.app.core.settings import config
from backend.app.core.exception_handler import add_exception_handlers
from backend.app.core.jwtmiddleware import JWTAuthMiddleware
from backend.app.api.v1.endpoints.home_routes import router as home_router
from backend.app.api.v1.endpoints.company_routes import router as company_router
from backend.app.api.v1.endpoints.auth_routes import router as auth_router
from backend.app.api.v1.endpoints.service.law_routes import router as law_router

logger = get_logger(__name__)


def set_middlewares(app: FastAPI):
    ''' 미들웨어 설정 '''
        # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # JWT 인증 미들웨어 등록
    app.add_middleware(JWTAuthMiddleware)



def set_routes(app: FastAPI):
    ''' 라우팅 설정 '''
    app.include_router(home_router) # 화면
    app.include_router(company_router, prefix="/api/v1/company", tags=["company"])
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    # service들
    app.include_router(law_router, prefix="/api/v1/law", tags=["law"])
    
def set_event_handlers(app: FastAPI):
    ''' 이벤트 핸들러 설정 '''
    pass
def set_static_files(app: FastAPI):
    ''' 정적 파일 설정 '''
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_files_path = os.path.join(BASE_DIR, 'frontend', 'public')
    logger.info('------------------------------------------------')
    logger.debug(f"BASE_DIR: {BASE_DIR}")
    logger.debug(f"static_files_path: {static_files_path}")
    logger.info('------------------------------------------------')
    app.mount("/public", StaticFiles(directory=static_files_path), name="public")
    
def set_exception_handlers(app: FastAPI):
    ''' 예외 처리 설정 '''
    add_exception_handlers(app)
        
def create_app() -> FastAPI:
    ''' FastAPI 앱 생성 '''
    service_title = config.SERVICE_TITLE
    logger.info('------------------------------------------------')
    logger.info(f"{service_title} 서버 시작")
    logger.info('------------------------------------------------')
    logger.info(f"API 문서: http://localhost:{config.SERVICE_PORT}/docs")
    logger.info(config)

    app = FastAPI(title=service_title, version="0.0.1")
    set_middlewares(app)
    set_routes(app)
    set_event_handlers(app)
    set_static_files(app)
    set_exception_handlers(app)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    service_port = config.SERVICE_PORT
    uvicorn.run(app, host="0.0.0.0", port=service_port, reload=True)