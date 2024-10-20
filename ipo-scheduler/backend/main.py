import os
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.core.logger import get_logger
from backend.app.domains.ipo.ipo_history_model import IpoHistory
from backend.app.domains.system.config_model import DbConfig
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.ipo.ipo_model import Ipo
from backend.app.domains.system.scheduler_job_model import SchedulerJob
from backend.app.domains.user.user_model import User
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.core.jwtmiddleware import JWTAuthMiddleware
from backend.app.api.v1.endpoints.user_routes import router as user_router
from backend.app.api.v1.endpoints.home_routes import router as home_router
from backend.app.api.v1.endpoints.eventdays_routes import router as eventdays_router
from backend.app.api.v1.endpoints.ipo_routes import router as ipo_router
from backend.app.api.v1.endpoints.scheduler_routes import router as scheduler_router
from backend.app.api.v1.endpoints.config_routes import router as config_router

from backend.app.core.scheduler import Scheduler
from backend.app.core.exception_handler import add_exception_handlers
from backend.app.core.dependency import get_scheduler_job_service 


logger = get_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title="IPO-scheduler", version="0.1.1")
    add_middlewares(app)
    add_routes(app)
    add_event_handlers(app)
    add_static_files(app)
    add_exception_handlers(app)
    return app

def add_middlewares(app: FastAPI):
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



def add_routes(app: FastAPI):
    # API 라우터 포함
    app.include_router(home_router) # 화면
    app.include_router(user_router, prefix="/api/v1/user", tags=["user"])
    app.include_router(eventdays_router, prefix="/api/v1/eventdays", tags=["eventdays"])
    app.include_router(ipo_router, prefix="/api/v1/ipo", tags=["ipo"])
    app.include_router(scheduler_router, prefix="/api/v1/scheduler", tags=["scheduler"])
    app.include_router(config_router, prefix="/api/v1/config", tags=["config"])

    

def add_event_handlers(app: FastAPI):
    ''' 이벤트 핸들러 설정 '''
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)

def add_static_files(app: FastAPI):
    ''' 정적 파일 설정 '''
    # static
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_files_path = os.path.join(BASE_DIR, 'frontend', 'public')
    app.mount("/public", StaticFiles(directory=static_files_path), name="public")

async def startup_event():
    ''' IPO-scheduler application  시작 '''
    logger.info('---------------------------------')
    logger.info('Startup 프로세스 시작')
    logger.info('---------------------------------')

    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    logger.info('---------------------------------')
    logger.info(f"MongoDB 연결: {mongodb_url}/{db_name}")
    logger.info('---------------------------------')
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
    await init_beanie(database=db, document_models=[EventDays])
    await init_beanie(database=db, document_models=[Ipo])
    await init_beanie(database=db, document_models=[IpoHistory])
    await init_beanie(database=db, document_models=[DbConfig])
    await init_beanie(database=db, document_models=[SchedulerJob])
    

    # 스케줄러 시작
    logger.info('---------------------------------')
    logger.info("스케줄러 시작")
    logger.info('---------------------------------')
    scheduler = Scheduler.get_instance()   
    scheduler.start()
    scheduler_service =  get_scheduler_job_service()
    await scheduler_service.register_system_jobs()

    # 자동매매 시작
    # await start_danta_machine()
    # Telegram Bot 시작
    
    # telegram_token, telegram_userid = await initialize_telegram_bot()
    # if telegram_token is not None:
    #     asyncio.create_task(start_telegram_bot())
    # else:
    #     logger.warning("TELEGRAM_BOT_TOKEN 이 존재하지 않음.")

    logger.info('---------------------------------')
    logger.info('Startup 프로세스 종료')
    logger.info('---------------------------------')


async def shutdown_event():
    ''' IPO-scheduler application 종료 '''
    logger.info('---------------------------------')
    logger.info('Shutdown 프로세스 시작')
    logger.info('---------------------------------')
    await MongoDb.close()
    logger.info("MongoDB 연결 해제")
    
    scheduler = Scheduler.get_instance()
    scheduler.shutdown()
    logger.info("스케줄러 종료")

    logger.info('---------------------------------')
    logger.info('Shutdown 프로세스 종료')
    logger.info('---------------------------------')

app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info("IPO-scheduler  서버 시작")
    uvicorn.run(app, host="0.0.0.0", port=8881, reload=True)
