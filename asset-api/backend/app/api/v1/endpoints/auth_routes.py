
from fastapi import APIRouter
from backend.app.core.logger import get_logger
logger = get_logger(__name__)

router = APIRouter()

@router.post("/register",  response_model=Company)
async def register():
    ''' 회사정보에 기반하여 app_key, secret_key를 만들고 Db에 저장한다. '''
    list = await ipo_service.get_all(onlyFuture=True)
    return list