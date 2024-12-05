import random
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.snote.snote_schema import SNoteResponse, SnoteCreateRequest, SnoteHintResponse, SnoteListRequest, SnoteListResponse
from app.domain.snote.snote_service import SNoteService


router = APIRouter()

DEFAULT_HINT_PW = [
    {"hint": "js의 생년월일", "password": "970226"},
    {"hint": "회사명군번느낌표", "password": "kalpa9732!"},
    {"hint": "할아버지산소", "password": "ansrud"},
    {"hint": "어머니의 고향", "password": "dorn"},
    {"hint": "출근방법은", "password": "Ekfmddl"},
]

@router.post("/snote", response_model=SNoteResponse)
async def upsert_snote(req: SnoteCreateRequest, db: AsyncSession = Depends(get_session)):
    """노트 생성/수정"""
    service = SNoteService(db)
    return await service.upsert_snote(req.id, req)

@router.get("/snote", response_model=SnoteListResponse)
async def get_snotes(
    search_text: str = None,
    start_index: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)):
    ''' 조회 '''
    req = SnoteListRequest(search_text=search_text, start_index=start_index, limit=limit)
    service = SNoteService(db)
    return await service.get_snotes(req)


@router.delete("/snote/{id}", response_model=SNoteResponse)
async def delete_snote(id:int, db: AsyncSession = Depends(get_session)):
    ''' id로 snote 1개 삭제 '''
    service = SNoteService(db)
    return await service.delete_snote(id)
    

@router.get("/snote/get-random-hint", response_model=SnoteHintResponse)
async def get_random_hint():
    # 랜덤 힌트와 비밀번호 선택
    selected = random.choice(DEFAULT_HINT_PW)
    # 비밀번호를 SHA256으로 해싱
    password = selected["password"]
    # 결과 반환
    response = SnoteHintResponse(hint=selected["hint"], password=password)
    
    return response

