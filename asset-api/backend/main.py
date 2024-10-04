from fastapi import FastAPI
from backend.app.core.logger import get_logger
from backend.app.core.settings import config

logger = get_logger(__name__)


def set_middlewares(app: FastAPI):
    ''' 미들웨어 설정 '''
    # JWT 인증 미들웨어 등록
    app.add_middleware(JWTAuthMiddleware)

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
def create_app() -> FastAPI:
    ''' FastAPI 앱 생성 '''
    service_title = config.SERVICE_TITLE
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
    service_title = config.SERVICE_TITLE
    logger.info('------------------------------------------------')
    logger.info(f"{service_title} 서버 시작")
    logger.info('------------------------------------------------')
    service_port = config.SEVICE_PORT
    uvicorn.run(app, host="0.0.0.0", port=service_port, reload=True)