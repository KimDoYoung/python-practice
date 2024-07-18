import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from beanie import init_beanie

from backend.app.background.danta_machine import start_danta_machine, stop_danta_machine
from backend.app.background.telegram_bot import initialize_telegram_bot, start_telegram_bot, stop_telegram_bot
from backend.app.core.logger import get_logger
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.core.jwtmiddleware import JWTAuthMiddleware
from backend.app.api.v1.endpoints import (
    user_routes,
    home_routes,
    eventdays_routes,
    ipo_routes,
    scheduler_routes,
    config_routes,
    kis_routes,
    mystock_routes,
    client_websocket_routes,
    danta_machine_routes
)
from backend.app.core.scheduler import Scheduler
from backend.app.core.exception_handler import add_exception_handlers
from backend.app.core.dependency import get_scheduler_job_service
from backend.app.domains.system import config_model, eventdays_model, ipo_model, mystock_model, scheduler_job_model
from backend.app.domains.user.user_model import User

logger = get_logger(__name__)

# Constants
MONGODB_URL = config.DB_URL
DB_NAME = config.DB_NAME
MODELS = [
    User,
    config_model.DbConfig,
    eventdays_model.EventDays,
    ipo_model.Ipo,
    mystock_model.MyStock,
    scheduler_job_model.SchedulerJob
]

def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""
    app = FastAPI(title="Lucy - 단타머신(개인용)")

    app.add_middleware(JWTAuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static files
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_FILES_PATH = os.path.join(BASE_DIR, 'frontend', 'public')
    app.mount("/public", StaticFiles(directory=STATIC_FILES_PATH), name="public")

    # Include routers
    include_routers(app)

    # Exception handlers
    add_exception_handlers(app)

    # Event handlers
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)

    return app

def include_routers(app: FastAPI):
    """Include all routers."""
    app.include_router(home_routes.router)
    app.include_router(user_routes.router, prefix="/api/v1/user", tags=["user"])
    app.include_router(eventdays_routes.router, prefix="/api/v1/eventdays", tags=["eventdays"])
    app.include_router(ipo_routes.router, prefix="/api/v1/ipo", tags=["ipo"])
    app.include_router(scheduler_routes.router, prefix="/api/v1/scheduler", tags=["scheduler"])
    app.include_router(config_routes.router, prefix="/api/v1/config", tags=["config"])
    app.include_router(kis_routes.router, prefix="/api/v1/kis", tags=["kis"])
    app.include_router(mystock_routes.router, prefix="/api/v1/mystock", tags=["mystock"])
    app.include_router(danta_machine_routes.router, prefix="/api/v1/danta", tags=["danta"])
    app.include_router(client_websocket_routes.router)

async def startup_event():
    """Application startup event."""
    logger.info('---------------------------------')
    logger.info('Starting up application')
    logger.info('---------------------------------')

    await initialize_database()
    await initialize_scheduler()
    await start_services()

    logger.info('---------------------------------')
    logger.info('Startup complete')
    logger.info('---------------------------------')

async def shutdown_event():
    """Application shutdown event."""
    logger.info('---------------------------------')
    logger.info('Shutting down application')
    logger.info('---------------------------------')

    await MongoDb.close()
    logger.info("Disconnected from MongoDB")

    Scheduler.get_instance().shutdown()
    logger.info("Scheduler stopped")

    await stop_services()

    logger.info('---------------------------------')
    logger.info('Shutdown complete')
    logger.info('---------------------------------')

async def initialize_database():
    """Initialize the database."""
    logger.info(f"Connecting to MongoDB: {MONGODB_URL} / {DB_NAME}")
    await MongoDb.initialize(MONGODB_URL)
    db = MongoDb.get_client()[DB_NAME]
    await init_beanie(database=db, document_models=MODELS)

async def initialize_scheduler():
    """Initialize and start the scheduler."""
    logger.info("Starting scheduler")
    scheduler = Scheduler.get_instance()
    scheduler.start()
    scheduler_service = get_scheduler_job_service()
    await scheduler_service.register_system_jobs()

async def start_services():
    """Start necessary services."""
    await start_danta_machine()
    telegram_token, telegram_userid = await initialize_telegram_bot()
    if telegram_token:
        asyncio.create_task(start_telegram_bot())
    else:
        logger.warning("TELEGRAM_BOT_TOKEN is not set.")

async def stop_services():
    """Stop all running services."""
    await stop_danta_machine()
    await stop_telegram_bot()

app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Lucy stock trading server")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
