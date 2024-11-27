# diary_routes.py
"""
모듈 설명: 
    -  일기 관련 API 라우터
주요 기능:
    - 일기생성 : POST, /diary
    - 일기 조회 : GET, /diary/{ymd}
    - 일기 목록 조회 : GET, /diaries
    - 일기 수정 : PUT, /diary/{ymd}
    - 일기 삭제 : DELETE, /diary/{ymd}
    - 일기 첨부파일 목록 조회 : GET, /diary/attachments/{ymd}
    - 일기 첨부파일 삭제 : DELETE, /diary/attachments/{ymd}/{node_id}

작성자: 김도영
작성일: 2024-10-27
버전: 1.0
"""
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.diary.diary_schema import DiaryBase, DiaryDetailResponse, DiaryPageModel, DiaryRequest, DiaryResponse, DiaryUpdateRequest
from app.domain.diary.diary_service import DiaryService
from fastapi import File, UploadFile
from typing import List, Optional
from app.core.database import get_session
from app.domain.filenode.filenode_schema import AttachFileInfo, FileNoteData

router = APIRouter()

@router.post("/diary/upsert", response_model=DiaryResponse)
async def upsert_diary(
    ymd: str = Form(...),
    content: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_session)
):
    ''' 일기 생성 또는 수정 '''
    service = DiaryService(db)
    try:
        diary_response = await service.upsert_diary(DiaryRequest(ymd=ymd, content=content, summary=summary))
        
        if not diary_response:
            raise HTTPException(status_code=500, detail="Failed to create diary entry.")
        
        return diary_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 일기생성
@router.post("/diary", response_model=DiaryResponse)
async def create_diary(
    ymd: str = Form(...),
    content: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),  # 여러 파일을 받을 수 있도록 설정, null 허용
    db: AsyncSession = Depends(get_session)
):
    service = DiaryService(db)
    try:
        diary_response = await service.create_diary(DiaryRequest(ymd=ymd, content=content, summary=summary), files)
        
        if not diary_response:
            raise HTTPException(status_code=500, detail="Failed to create diary entry.")
        
        return diary_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Get diary by ymd
@router.get("/diary/{ymd}", response_model=DiaryDetailResponse)
async def get_diary(ymd: str, db: AsyncSession = Depends(get_session)):
    ''' diary 1개 조회, 달려있는 이미지 리스트도 함께 조회 '''
    service = DiaryService(db)
    diary = await service.get_diary(ymd)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return diary   

# 날짜 범위로 일기 목록 조회
@router.get("/diaries", response_model=DiaryPageModel)
async def get_diaries(
    start_ymd: str = "19000101",
    end_ymd: str = "99991231",
    start_index: int = 0,
    limit: int = 10,
    order: str = "desc",
    summary_only: bool = False,
    search_text = "",
    db: AsyncSession = Depends(get_session)
):
    '''날짜와 검색어로 일기 목록 조회'''
    service = DiaryService(db)
    return await service.get_diaries(start_ymd, end_ymd, start_index, limit=limit, order=order, summary_only=summary_only, search_text=search_text)

# Update diary
@router.put("/diary/{ymd}", response_model=DiaryBase)
async def update_diary(ymd: str, diary_data: DiaryUpdateRequest, db: AsyncSession = Depends(get_session)):
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

# 일기에 첨부파일 추가
@router.post("/diary/attachments/{ymd}", response_model=List[AttachFileInfo])
async def add_diary_attachments(ymd: str, files: List[UploadFile] = File(None), db: AsyncSession = Depends(get_session)):
    ''' 일지에 파일들 첨부 '''
    service = DiaryService(db)
    result =  await service.add_diary_attachments(ymd, files)
    # 성공시 목록 
    if result:
        return await service.get_diary_attachments_urls(ymd)
    else:
        raise HTTPException(status_code=500, detail="Failed to add attachments")


# 일기에 첨부된 파일목록 조회
@router.get("/diary/attachments/{ymd}", response_model=List[AttachFileInfo])
async def get_diary_attachments(ymd: str, db: AsyncSession = Depends(get_session)):
    ''' 일지에 첨부된 파일 목록 조회 '''
    service = DiaryService(db)
    return await service.get_diary_attachments_urls(ymd)

# 첨부파일 삭제
@router.delete("/diary/attachments/{ymd}/{node_id}", response_model=dict)
async def get_diary_delete_attachment(ymd: str, node_id : str,  db: AsyncSession = Depends(get_session)):
    ''' 일지에 첨부된 파일 1개를 삭제 '''
    service = DiaryService(db)
    return await service.get_diary_delete_attachment(ymd, node_id)

# 첨부파일 이미지에 노트 기입
@router.put("/diary/attachments/note", response_model=dict)
async def get_diary_delete_attachment(note_data : FileNoteData,  db: AsyncSession = Depends(get_session)):
    ''' 일지에 첨부된 파일 1개에 노트(코멘트)를 기입 '''
    service = DiaryService(db)
    ap_file =  await service.set_diary_attachment_note(note_data)
    if not ap_file:
        raise HTTPException(status_code=404, detail="File not found")
    return {"node_id" : ap_file.node_id, "file_name" : ap_file.org_file_name, "note" : ap_file.note}