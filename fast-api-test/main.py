from fastapi import FastAPI
from api.v1.item_routes import router as item_router
from core.database import init_db

app = FastAPI()

app.include_router(item_router)

@app.on_event("startup")
async def startup_event():
    await init_db(app)
