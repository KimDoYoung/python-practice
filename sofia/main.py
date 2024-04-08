from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.v1.home import router as home_router
from api.v1.image_folder import router as folder_router
from db import db_session

app = FastAPI()




def configure(dev_mode: bool):
    """
    template, routers, database connection 설정
    """
    configure_routers()
    configure_db(dev_mode)


def configure_routers():
    '''
    라우터 설정
    '''
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home_router)
    app.include_router(folder_router)

def configure_db(dev_mode):
    '''
    데이터베이스 설정
    '''
    file = (Path(__file__).parent / "data" / "sofia.sqlite").absolute()
    db_session.global_init(file.as_posix())  # 데이터베이스 초기화


def main():
    import uvicorn
    configure(dev_mode=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
else:
    configure(dev_mode=False)

