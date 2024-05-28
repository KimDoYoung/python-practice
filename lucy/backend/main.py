import os
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.domains.system.config_model import DbConfig
from backend.app.domains.system.eventdays_model import EventDays
from backend.app.domains.system.ipo_model import Ipo
from backend.app.domains.user.user_model import User
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.core.jwtmiddleware import JWTAuthMiddleware
from backend.app.api.v1.endpoints.user_routes import router as user_router
from backend.app.api.v1.endpoints.home_routes import router as home_router
from backend.app.api.v1.endpoints.eventdays_routes import router as eventdays_router
from backend.app.api.v1.endpoints.ipo_routes import router as ipo_router


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
    mongodb_url = config.DB_URL 
    db_name = config.DB_NAME

    await MongoDb.initialize(mongodb_url)
    
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
    await init_beanie(database=db, document_models=[EventDays])
    await init_beanie(database=db, document_models=[Ipo])
    await init_beanie(database=db, document_models=[DbConfig])
    
async def shutdown_event():
    await MongoDb.close()

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
app.include_router(eventdays_router)
app.include_router(ipo_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
