import os
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.app.api.v1.endpoints.stc import korea_investment
from backend.app.api.v1.endpoints.openapi import datagokr
from backend.app.api.v1.endpoints.openapi import dart
from backend.app.api.v1.endpoints import user
from backend.app.api.v1.endpoints import appkeys
from backend.app.api.v1.endpoints import home
from backend.app.core.logger import get_logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.core.exception_handler import custom_404_exception_handler, general_exception_handler, http_exception_handler, validation_exception_handler

logger = get_logger(__name__)

app = FastAPI()


def main():
    configure(dev_mode=True)
    uvicorn.run(app, host='127.0.0.1", port=8000', debug=True )

def configure(dev_mode: bool):
    # pass
    # configure_templates(dev_mode)
    configure_routes()
    # configure_db(dev_mode)
    configure_exception_handlers()

def configure_exception_handlers():
    """FastAPI 앱에 예외 핸들러를 등록하는 함수"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    app.add_exception_handler(StarletteHTTPException, custom_404_exception_handler)
            
def configure_db(dev_mode: bool):
    pass
    # file = (Path(__file__).parent / 'db' / 'pypi.sqlite').absolute()
    # db_session.global_init(file.as_posix())


def configure_templates(dev_mode: bool):
    pass
    # fastapi_chameleon.global_init('templates', auto_reload=dev_mode)


def configure_routes():
    # 현재 파일(main.py)의 위치를 기준으로 상대 경로를 구성합니다.
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_files_path = os.path.join(BASE_DIR, 'frontend', 'public')
    app.mount("/public", StaticFiles(directory=static_files_path), name="public")
    app.include_router(korea_investment.router)
    app.include_router(datagokr.router)
    app.include_router(dart.router)
    app.include_router(user.router)
    app.include_router(appkeys.router)
    app.include_router(home.router)
    # app.include_router(account.router)
    # app.include_router(packages.router)

if __name__ == '__main__':
    main()
else:
    configure(dev_mode=False)
