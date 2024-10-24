from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import get_logger
from app.core.settings import config
from app.core.exception_handler import add_exception_handlers
from app.core.middleware import Middleware

from app.api.v1.endpoints.diary_routes import router as diary_router

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
    app.add_middleware(Middleware)



def set_routes(app: FastAPI):
    ''' 라우팅 설정 '''
    app.include_router(diary_router, prefix="/api/v1", tags=["diary"])
    
def set_event_handlers(app: FastAPI):
    ''' 이벤트 핸들러 설정 '''
    pass
    
def set_static_files(app: FastAPI):
    ''' 정적 파일 설정 '''
    pass

    
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