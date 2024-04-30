from fastapi import FastAPI

from app.core.mongodb import MongoDb
from app.domain.users.user_routes import user_router
from app.domain.users.user_service import UserService


app = FastAPI(title="FastAPI with MongoDB", description="FastAPI with MongoDB", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    MongoDb.initialize('mongodb://root:root@test.kfs.co.kr:27017/')
    try:
        app.state.user_service = await UserService.create_instance(db_client=MongoDb.get_client())
        print("User service created successfully")
    except Exception as e:
        print("----> user_service 실패:" , e)
    

@app.on_event("shutdown")
async def shutdown_event():
    MongoDb.close()

app.include_router(user_router, prefix="/api/v1", tags=["users"])

