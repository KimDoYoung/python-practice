from fastapi import FastAPI

from app.core.dependency import get_database, init_beanie, initialize_beanie
from app.core.mongodb import MongoDb
from app.domain.users.user_routes import user_router
from app.domain.users.user_service import UserService


app = FastAPI(title="FastAPI with MongoDB", description="FastAPI with MongoDB", version="0.1.0")

async def startup_event():
    db_url = 'mongodb://root:root@test.kfs.co.kr:27017/'
    db_name = 'stockdb'
    db = await get_database(db_url, db_name)
    await initialize_beanie(db)

async def shutdown_event():
    MongoDb.close()

# Adding event handlers to the application lifecycle
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

app.include_router(user_router, prefix="/api/v1", tags=["users"])
