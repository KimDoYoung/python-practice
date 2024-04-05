from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.databases import DatabaseConnection
from controllers.home import router as home_router

app = FastAPI()

# 데이터베이스 URL 설정
DATABASE_URL = "sqlite:///./db/sofia.sqlite"
db_connection = DatabaseConnection(DATABASE_URL)

# 정적 파일과 템플릿 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    await db_connection.connect()
    await db_connection.create_tables()    

@app.on_event("shutdown")
async def shutdown():
    await db_connection.disconnect()

# 라우터 등록
app.include_router(home_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8181)
