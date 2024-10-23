from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.diary.diary_schema import DiaryRequest, DiaryListResponse
from app.domain.diary.diary_service import DiaryService
from app.core.database import get_session

router = APIRouter()

# Create diary
@router.post("/diary", response_model=DiaryListResponse)
async def create_diary(diary_data: DiaryRequest, db: AsyncSession = Depends(get_session)):
    service = DiaryService(db)
    return await service.create_diary(diary_data)

# Get diary by ymd
@router.get("/diary/{ymd}", response_model=DiaryListResponse)
async def get_diary(ymd: str, db: AsyncSession = Depends(get_session)):
    ''' diary 1개 조회, 달려있는 이미지 리스트도 함께 조회 '''
    service = DiaryService(db)
    diary = await service.get_diary(ymd)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary   

# 날짜 범위로 일기 목록 조회
@router.get("/diaries", response_model=dict)
async def get_diaries(
    start_ymd: str = "19000101",
    end_ymd: str = "99991231",
    start_index: int = 0,
    limit: int = 10,
    order: str = "desc",
    summary_only: bool = False,
    db: AsyncSession = Depends(get_session)
):
    service = DiaryService(db)
    return await service.get_diaries(start_ymd, end_ymd, start_index, limit=limit, order=order, summary_only=summary_only)

# Update diary
@router.put("/diary/{ymd}", response_model=DiaryListResponse)
async def update_diary(ymd: str, diary_data: DiaryRequest, db: AsyncSession = Depends(get_session)):
    service = DiaryService(db)
    updated_diary = await service.update_diary(ymd, diary_data)
    if not updated_diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return updated_diary

# Delete diary
@router.delete("/diary/{ymd}", response_model=bool)
async def delete_diary(ymd: str, db: AsyncSession = Depends(get_session)):
    ''' 일지 1개를 삭제 '''
    service = DiaryService(db)
    success = await service.delete_diary(ymd)
    if not success:
        raise HTTPException(status_code=404, detail="Diary not found")
    return success
