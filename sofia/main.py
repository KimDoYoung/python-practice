from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1.home_routes import router as home_router
from api.v1.image_folder_routes import router as folder_router
from core.database import global_init

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    #file = (Path(__file__).parent / "data" / "sofia.sqlite").absolute()
    await global_init()  # 데이터베이스 초기화

def configure(dev_mode: bool):
    """
    routers 설정
    """
    configure_routers()


def configure_routers():
    '''
    라우터 설정
    '''
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home_router)
    app.include_router(folder_router)

# def configure_db(dev_mode):
#     '''
#     데이터베이스 설정
#     '''
    #file = (Path(__file__).parent / "data" / "sofia.sqlite").absolute()
    #await db_session.global_init(file.as_posix())  # 데이터베이스 초기화


def main():
    import uvicorn
    configure(dev_mode=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
else:
    configure(dev_mode=False)

