import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from beanie import init_beanie


from backend.app.domains.logs.logs_model import Logs
from backend.app.domains.settings.settings_model import Settings
from backend.app.domains.user.user_model import User
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.api.v1.endpoints import (
    stock_kis_routes, user_routes, home_routes, websocket_routes
)
from backend.app.core.exception_handler import add_exception_handlers
from backend.app.core.logger import get_logger
# from backend.app.core.globals import client_ws_manager, stock_ws_manager, api_manager

logger = get_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title="Stock API", version="0.1.0")
    add_middlewares(app)
    add_routes(app)
    add_event_handlers(app)
    add_static_files(app)
    add_exception_handlers(app)
    return app

def add_middlewares(app: FastAPI):
    ''' 미들웨어 설정 '''
    #app.add_middleware(JWTAuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def add_routes(app: FastAPI):
    ''' 라우터 설정'''
    app.include_router(home_routes.router) # 화면
    app.include_router(user_routes.router, prefix="/api/v1/user", tags=["user"])
    app.include_router(stock_kis_routes.router, prefix="/api/v1/kis", tags=["kis"])
    app.include_router(websocket_routes.router, prefix="/api/v1", tags=["websocket"])

def add_static_files(app: FastAPI):
    '''정적 파일 경로 설정'''
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_files_path = os.path.join(BASE_DIR, 'frontend', 'public')
    app.mount("/public", StaticFiles(directory=static_files_path), name="public")

def add_event_handlers(app: FastAPI):
    ''' start/shutdown 이벤트 핸들러 등록'''
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)

async def startup_event():
    global client_ws_manager, stock_ws_manager, api_manager
    logger.info('---------------------------------')
    logger.info('Startup 프로세스 시작')
    logger.info('---------------------------------')

    mongodb_url = config.DB_URL
    db_name = config.DB_NAME
    logger.info(f"MongoDB 연결: {mongodb_url} / {db_name}")
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[
        User, Settings, Logs
    ])

    logger.info('---------------------------------')
    logger.info('Startup 프로세스 종료')
    logger.info('---------------------------------')

async def shutdown_event():
    logger.info('---------------------------------')
    logger.info('Shutdown 프로세스 시작')
    logger.info('---------------------------------')
    await MongoDb.close()
    logger.info("MongoDB 연결 해제")
    
    logger.info('---------------------------------')
    logger.info('Shutdown 프로세스 종료')
    logger.info('---------------------------------')

app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info("KFS Stock-API 서버 시작")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
