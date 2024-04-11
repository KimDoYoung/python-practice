from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1.home_routes import router as home_router
from api.v1.image_folder_routes import router as folder_router
from api.v1.image_file_routes import router as file_router
from core.database import global_init

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    애플리케이션 시작 시 필요한 초기화 수행
    """
    await global_init()  # 데이터베이스 초기화

def configure():
    """
    애플리케이션 구성: 라우터 및 기타 설정
    """
    configure_routers()

def configure_routers():
    """
    라우터 설정: API 엔드포인트 및 정적 파일 서빙
    """
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home_router)
    app.include_router(folder_router)
    app.include_router(file_router)

def main():
    import uvicorn
    configure()
    uvicorn.run(app, host="0.0.0.0", port=8181)

if __name__ == '__main__':
    main()
