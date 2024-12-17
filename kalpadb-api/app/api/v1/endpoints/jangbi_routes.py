# diary_routes.py
"""
모듈 설명: 
    -  장비(구매물품) 관련 API 라우터
주요 기능:

작성자: 김도영
작성일: 2024-11-28
버전: 1.0
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.filenode.filenode_schema import AttachFileInfo
from app.domain.jangbi.jangbi_schema import JangbiListParam, JangbiResponse, JangbiUpsertRequest
from app.domain.jangbi.jangbi_service import JangbiService

router = APIRouter()

@router.get("/jangbies", summary="장비리스트 페이지 조회", response_model=JangbiListResponse)
async def get_jangbi_list(
    start_ymd: str = '19700101',
    end_ymd: str = '99991231',
    search_text : str | None = None,
    lvl : str | None = None,
    order_direction : str = 'desc',
    start_idx : int = 0,
    limit : int = 10,
    db: AsyncSession = Depends(get_session)
):
    ''' 장비 리스트 조회 '''
    service = JangbiService(db)
    param = JangbiListParam(
        start_ymd=start_ymd,
        end_ymd=end_ymd,
        search_text=search_text,
        lvl=lvl,
        order_direction=order_direction,
        start_idx=start_idx,
        limit=limit
    )
    return await service.jangbi_list(param)

@router.get("/jangbi/{jangbi_id}",summary="장비 1개 조회", response_model=JangbiResponse)
async def get_jangbi(
    jangbi_id: int,
    db: AsyncSession = Depends(get_session)
):
    ''' 장비 1개 조회 첨부파일 포함 '''
    service = JangbiService(db)
    return await service.get_jangbi_by_id(jangbi_id)

@router.post("/jangbi",summary="장비1개 UPDATE OR INSERT", response_model=JangbiResponse)
async def upsert_jangbi( request: JangbiUpsertRequest, db: AsyncSession = Depends(get_session)):
    ''' 장비 생성 또는 수정 '''
    service = JangbiService(db)
    jangbi_response = await service.upsert_jangbi(request)
    if not jangbi_response:
        raise HTTPException(status_code=500, detail="Failed to create jangbi entry.")
    return jangbi_response

@router.delete("/jangbi/{jangbi_id}",summary="장비1개 삭제", response_model=JangbiResponse)
async def delete_jangbi(jangbi_id: int, db: AsyncSession = Depends(get_session)):
    ''' 장비 삭제 '''
    service = JangbiService(db)
    jangbi_response = await service.delete_jangbi(jangbi_id)
    if not jangbi_response:
        raise HTTPException(status_code=404, detail="Jangbi not found.")
    return jangbi_response

@router.post("/jangbi/attach/{jangbi_id}", summary="장비에 첨부파일들 추가", response_model=List[AttachFileInfo])
async def attach_files_jangbi(jangbi_id: int, files: List[UploadFile], db: AsyncSession = Depends(get_session)):
    ''' 장비 첨부파일 추가 '''
    service = JangbiService(db)
    result = await service.add_jangbi_attachments(jangbi_id, files)
    # 성공시 목록 
    if result:
        return await service.get_jangbi_attachments_urls(jangbi_id)
    else:
        raise HTTPException(status_code=500, detail="Failed to add attachments")

# 첨부파일 삭제
@router.delete("/jangbi/attachments/{jangbi_id}/{node_id}", summary="장비의 첨부파일1개 삭제", response_model=dict)
async def delete_attachment(jangbi_id: str, node_id : str,  db: AsyncSession = Depends(get_session)):
    ''' 장비에 첨부된 파일 1개를 삭제 '''
    service = JangbiService(db)
    return await service.delete_attachment(jangbi_id, node_id)