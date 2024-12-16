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

@router.post("/snote",summary="snote 1개를 insert or update", response_model=SNoteResponse)
async def upsert_snote(req: SnoteCreateRequest, db: AsyncSession = Depends(get_session)):
    """노트 생성/수정"""
    service = SNoteService(db)
    return await service.upsert_snote(req.id, req)

@router.get("/snote", summary="snote 페이지 조회", response_model=SnoteListResponse)
async def get_snotes(
    search_text: str = None,
    start_index: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_session)):
    ''' 페이지 조회 '''
    req = SnoteListRequest(search_text=search_text, start_index=start_index, limit=limit)
    service = SNoteService(db)
    return await service.get_snotes(req)

@router.get("/snote/{id}",summary="snote 1개를 조회", response_model=SNoteResponse)
async def get_1_snote(id:int, db: AsyncSession = Depends(get_session)):
    ''' id로 snote 1개 조회 '''
    service = SNoteService(db)
    return await service.get_snote(id)


@router.delete("/snote/{id}", summary="snote 1개를 삭제", response_model=SNoteResponse)
async def delete_snote(id:int, db: AsyncSession = Depends(get_session)):
    ''' id로 snote 1개 삭제 '''
    service = SNoteService(db)
    return await service.delete_snote(id)
    

@router.get("/snote/get-random-hint", summary="랜덤 암호화 힌트 제공",response_model=SnoteHintResponse)
async def get_random_hint():
    # 랜덤 힌트와 비밀번호 선택
    selected = random.choice(DEFAULT_HINT_PW)
    # 비밀번호를 SHA256으로 해싱
    password = selected["password"]
    # 결과 반환
    response = SnoteHintResponse(hint=selected["hint"], password=password)
    
    return response

