
from fastapi import APIRouter

from backend.app.domains.stc.korea_investment.korea_investment_service import get_access_token


router = APIRouter()

@router.get("/stc/korea_investment/test1")
async def korea_investment_test1():
    ACCESS_TOKEN = get_access_token();
    logger.debug(f"ACCESS_TOKEN:{ACCESS_TOKEN}")
    
    return {"message": "Korea Investmenet test1"}

