from beanie import init_beanie
from fastapi import FastAPI
from app.core.mongodb import MongoDb
from app.domain.users.user_model import User
from app.domain.users.user_routes import user_router
from app.domain.users.user_service import UserService


app = FastAPI(title="FastAPI with MongoDB", description="FastAPI with MongoDB", version="0.1.0")

async def startup_event():
    mongodb_url = 'mongodb://root:root@test.kfs.co.kr:27017/'
    db_name = 'stockdb'
    await MongoDb.initialize(mongodb_url)
    db = MongoDb.get_client()[db_name]
    await init_beanie(database=db, document_models=[User])
    
async def shutdown_event():
    await MongoDb.close()

# Adding event handlers to the application lifecycle
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

app.include_router(user_router, prefix="/api/v1", tags=["users"])
