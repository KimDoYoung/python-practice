from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.logger import get_logger
from app.domain.diary.diary_schema import DiaryRequest, DiaryResponse
from app.domain.diary.diary_service import DiaryService


logger = get_logger(__name__)

router = APIRouter()

# 일기 작성
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary_req: DiaryRequest, db: Session = Depends(get_session)):
    service = DiaryService(db)
    return await service.create_diary(diary_req)

# 특정 일자 일기 조회
@router.get("/{ymd}", response_model=DiaryResponse)
async def get_diary(ymd: str, db: Session = Depends(get_session)):
    service = DiaryService(db)
    diary = await service.get_diary(ymd)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary

# 일기 업데이트
@router.put("/{ymd}", response_model=DiaryResponse)
async def update_diary(ymd: str, diary_data: DiaryRequest, db: Session = Depends(get_session)):
    service = DiaryService(db)
    updated_diary = await service.update_diary(ymd, diary_data)
    if not updated_diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return updated_diary

# 일기 삭제
@router.delete("/{ymd}", response_model=bool)
async def delete_diary(ymd: str, db: Session = Depends(get_session)):
    service = DiaryService(db)
    success = await service.delete_diary(ymd)
    if not success:
        raise HTTPException(status_code=404, detail="Diary not found")
    return success