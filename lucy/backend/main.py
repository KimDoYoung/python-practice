import os
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler

from backend.app.core.logger import get_logger
from backend.app.domains.system.config_model import DbConfig
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.ipo_model import Ipo
from backend.app.domains.system.scheduler_job_model import SchedulerJob
from backend.app.domains.system.scheduler_job_service import SchedulerJobService
from backend.app.domains.user.user_model import User
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.core.jwtmiddleware import JWTAuthMiddleware
from backend.app.api.v1.endpoints.user_routes import router as user_router
from backend.app.api.v1.endpoints.home_routes import router as home_router
from backend.app.api.v1.endpoints.eventdays_routes import router as eventdays_router
from backend.app.api.v1.endpoints.ipo_routes import router as ipo_router
from backend.app.api.v1.endpoints.scheduler_routes import router as scheduler_router

from backend.app.core.scheduler import Scheduler
from backend.app.scheduler.jobs.job_test import test1


logger = get_logger(__name__)

app = FastAPI(title="Lucy Project - 공모주청약(개인용)")
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

async def startup_event():
    ''' Lucy application  시작 '''

    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME
    logger.info(f"MongoDB 연결: {mongodb_url} / {db_name}")
    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
    await init_beanie(database=db, document_models=[EventDays])
    await init_beanie(database=db, document_models=[Ipo])
    await init_beanie(database=db, document_models=[DbConfig])
    await init_beanie(database=db, document_models=[SchedulerJob])

    # 스케줄러 시작
    logger.info("스케줄러 시작")
    scheduler = Scheduler.get_instance()   
    scheduler.start()
    scheduler_service = SchedulerJobService(scheduler=scheduler)
    await scheduler_service.register_system_jobs()
    # test_job = SchedulerJob.find_one({"job_id": "test_job"})
    # count = await test_job.count()
    # if count == 0:
    #     test_Job = SchedulerJob(job_id="test_job", job_name="test1", job_type="cron", run_type="cron", func_name="test1", cron="*/5 * * * *", args=["Hello, World!"])
    #     await test_Job.insert()
    
    
async def shutdown_event():
    ''' Lucy application 종료 '''
    await MongoDb.close()
    logger.info("MongoDB 연결 해제")
    
    scheduler = Scheduler.get_instance()
    scheduler.shutdown()
    logger.info("스케줄러 종료")

# Adding event handlers to the application lifecycle
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# static
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_files_path = os.path.join(BASE_DIR, 'frontend', 'public')
app.mount("/public", StaticFiles(directory=static_files_path), name="public")

# API 라우터 포함
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(home_router)
app.include_router(eventdays_router, prefix="/api/v1/eventdays", tags=["eventdays"])
app.include_router(ipo_router, prefix="/api/v1/ipo", tags=["ipo"])
app.include_router(scheduler_router,prefix="/api/v1/scheduler", tags=["scheduler"])

if __name__ == "__main__":
    import uvicorn
    logger.info("Lucy 자동주식매매 서버 시작")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
