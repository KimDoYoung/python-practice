from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.api.v1.endpoints.stc import korea_investment
from backend.app.api.v1.endpoints.openapi import datagokr
from backend.app.api.v1.endpoints.openapi import dart
from backend.app.api.v1.endpoints import user
from backend.app.api.v1.endpoints import appkeys
from backend.app.api.v1.endpoints import home
from backend.app.core.logger import get_logger
from backend.app.core.database_session_manager import sessionmanager
from backend.app.core.exception_handler import (
    custom_404_exception_handler, general_exception_handler, http_exception_handler, validation_exception_handler)

logger = get_logger(__name__)

app = FastAPI(title="Stock API", description="주식 관련 API", version="0.1.0")

@asynccontextmanager
async def lifespan_context():
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

def main():
    configure(dev_mode=True)
    app.lifespan = lifespan_context
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

def configure(dev_mode: bool):
    configure_routes()
    configure_exception_handlers()

def configure_exception_handlers():
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, custom_404_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

def configure_routes():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_files_path = os.path.join(BASE_DIR, 'frontend', 'public')
    app.mount("/public", StaticFiles(directory=static_files_path), name="public")
    app.include_router(korea_investment.router)
    app.include_router(datagokr.router)
    app.include_router(dart.router)
    app.include_router(user.router)
    app.include_router(appkeys.router)
    app.include_router(home.router)

if __name__ == '__main__':
    main()
