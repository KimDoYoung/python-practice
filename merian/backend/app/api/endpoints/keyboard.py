import json
import os
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.security import get_current_user
from backend.app.models.keyboard import FBFile, FileCollectionMatch, KeyboardModel
from backend.app.schemas.keyboard_schema import FBFileResponse, KeyboardCreateRequest, KeyboardResponse, KeyboardUpdateRequest, KeyboardRequest
from backend.app.services.keyboard_service import delete_physical_file, save_upload_file
from backend.app.core.logger import get_logger
from backend.app.utils.PageAttr import PageAttr
from backend.app.utils.cookies_util import get_cookie, set_cookie
from ...services.db_service import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks

logger = get_logger(__name__)

router = APIRouter()

#
#  리스트 조회
#
@router.get("/keyboard")
async def read_keyboards(request: Request, response: Response, # 수정됨
                        currentPageNo: Optional[int] = None, 
                        pageSize: Optional[int] = None, 
                        searchText: Optional[str] = None,
                        db: AsyncSession = Depends(get_db),
                        current_user_id: str = Depends(get_current_user)):

    query_attr = get_cookie(request, "query_attr", "{}") # 수정됨
    currentPageNo = query_attr.get('currentPageNo', currentPageNo or 1)
    pageSize = query_attr.get('pageSize', pageSize or 10)
    searchText = query_attr.get('searchText', searchText or "")

    set_cookie(response, "query_attr", {"currentPageNo": currentPageNo, "pageSize": pageSize, "searchText": searchText})

    skip = (currentPageNo - 1) * pageSize
    limit = pageSize 
    async with db as session:
        # 기본 쿼리 설정
        base_query = select(
            KeyboardModel.id,
            KeyboardModel.product_name,
            KeyboardModel.manufacturer,
            KeyboardModel.purchase_date,
            KeyboardModel.purchase_amount,
            KeyboardModel.key_type,
            KeyboardModel.switch_type,
            KeyboardModel.actuation_force,
            KeyboardModel.interface_type,
            KeyboardModel.overall_rating,
            KeyboardModel.typing_feeling,
            KeyboardModel.create_on,
            KeyboardModel.create_by,
            func.count(FileCollectionMatch.file_id).label('file_count')
        ).outerjoin(
            FileCollectionMatch, KeyboardModel.id == FileCollectionMatch.id
        ).group_by(KeyboardModel.id)
        
        # 검색 조건 적용
        if searchText:
            search_condition = or_(
                KeyboardModel.product_name.like(f"%{searchText}%"),
                KeyboardModel.manufacturer.like(f"%{searchText}%")
            )
            base_query = base_query.filter(search_condition)
        
        # totalCount를 구하기 위한 쿼리
        count_query = select(func.count('*')).select_from(base_query.subquery())
        total_count_result = await session.execute(count_query)
        totalCount = total_count_result.scalar_one()

        
        # 실제 데이터 조회 쿼리에 limit와 offset 적용
        query = base_query.order_by(KeyboardModel.create_by.desc()).offset(skip).limit(limit)
        keyboards_info = await session.execute(query)
        result =  keyboards_info.mappings().all()
        # 결과 변환
        keyboard_list = [
            {
                'id': kb.id, 
                'product_name': kb.product_name, 
                'manufacturer': kb.manufacturer,
                'purchase_date': kb.purchase_date,
                'purchase_amount': kb.purchase_amount,
                'key_type': kb.key_type,
                'switch_type': kb.switch_type,
                'actuation_force': kb.actuation_force,
                'interface_type': kb.interface_type,
                'overall_rating': kb.overall_rating,
                'typing_feeling': kb.typing_feeling,
                'create_on': kb.create_on,
                'create_by': kb.create_by,
                "file_count": kb.file_count if kb.file_count is not None else 0                
            } for kb in result
        ]
        
        #json_compatible_keyboard_list = jsonable_encoder(keyboard_list)
        json_compatible_keyboard_list = jsonable_encoder(keyboard_list)
        pageAttr = PageAttr(totalCount, pageSize, currentPageNo)
        pageAttrJson = pageAttr.to_json()

        response.set_cookie("name", "123")



        return JSONResponse(content={
            "list": json_compatible_keyboard_list, 
            "pageAttr": pageAttrJson,
            "searchText": searchText
        })

# 단일 조회
@router.get("/keyboard/{keyboard_id}", response_model=KeyboardResponse)
async def read_keyboard_with_files(
    keyboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)  # JWT 토큰에서 사용자 ID 추출
):
    async with db as session:
        keyboard_result = await session.execute(select(KeyboardModel).filter(KeyboardModel.id == keyboard_id))
        keyboard = keyboard_result.scalars().first()
        if not keyboard:
            raise HTTPException(status_code=404, detail="Keyboard not found")

        file_results = await session.execute(
            select(FBFile)
            .join(FileCollectionMatch, FileCollectionMatch.file_id == FBFile.file_id)
            .where(FileCollectionMatch.id == keyboard_id)
            .where(FileCollectionMatch.category == "keyboard")
        )
        files = file_results.scalars().all()

        # 파일 정보를 Pydantic 모델로 변환
        file_responses: List[FBFileResponse] = [FBFileResponse.from_orm(file) for file in files]

        # 최종 응답 구성
        response = KeyboardResponse.from_orm(keyboard)
        response.files = file_responses  # KeyboardResponse 스키마에 files 필드 추가 필요
        logger.debug(response.model_dump_json())
        return response    

# keyboard DB에 추가
@router.post("/keyboard/insert", response_model=KeyboardResponse)
async def create_keyboard(
    keyboardData: str = Form(...),
    db: AsyncSession = Depends(get_db),  # 여기를 수정
    current_user_id: str = Depends(get_current_user),  # JWT 토큰에서 사용자 ID 추출
    files: List[UploadFile] = None
):
    try:
        data = json.loads(keyboardData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    logger.debug("INSERT : 입력받은 데이터:" + json.dumps(data))
    new_keyboard_id=None
    # 올바르게 세션을 얻기 위한 변경
    async with db as session:
        async with session.begin():
            try:
                keyboard_request = KeyboardCreateRequest(**data)    
                keyboard_db = KeyboardModel(**keyboard_request.dict())
                keyboard_db.create_by = current_user_id  # 현재 사용자 ID로 생성자 정보 추가
                session.add(keyboard_db)
                await session.flush()  # 트랜잭션 커밋으로 데이터베이스에 반영
                print(keyboard_db.id)
                new_keyboard_id = keyboard_db.id
                if files:
                    for file in files:
                        # 파일 저장 및 파일 경로, 크기, MIME 타입 받기
                        physical_folder, physical_filename, extension, file_size, mime_type = await save_upload_file(file)
                        org_name = file.filename
                        # 파일 메타데이터와 경로를 사용하여 FBFile 인스턴스 생성
                        db_file = FBFile(
#                            file_id=keyboard_db.id,
                            node_id=keyboard_db.id,
                            phy_folder=physical_folder,
                            phy_name=physical_filename,
                            org_name=org_name,
                            ext=extension,
                            file_size=file_size,
                            mime_type=mime_type,  # 파일의 MIME 타입 추가
                            create_by=current_user_id  # 현재 사용자 ID로 생성자 정보 추가
                        )
                        session.add(db_file)
                        await session.flush()  # db_file의 file_id를 생성하기 위해 flush 호출

                        # file_collection_match 테이블에 데이터 추가
                        db_fcm = FileCollectionMatch(
                            id=keyboard_db.id, 
                            file_id=db_file.file_id,
                        )
                        session.add(db_fcm)
                        await session.flush()  # db_fcm의 id를 생성하기 위해 flush 호출
                await session.commit()  # 최종 커밋
            except Exception as e:
                await session.rollback()  # 오류 발생 시 롤백
                raise e
    # 업데이트된 키보드 정보를 바탕으로 KeyboardResponse 생성
    keyboard_response = await get_keyboard_response(session, new_keyboard_id)
    return keyboard_response             

#
# keyboard 수정
#
@router.put("/keyboard/{keyboard_id}", response_model=KeyboardResponse)
async def update_keyboard(
    keyboard_id: int,
    keyboardFormData: str = Form(...),
    files: List[UploadFile] = File(default=[]),  # 추가할 파일
    current_user_id: str = Depends(get_current_user),  # JWT 토큰에서 사용자 ID 추출
    db: AsyncSession = Depends(get_db)
):
    try:
        data = json.loads(keyboardFormData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    logger.debug("UPDATE : 입력받은 데이터:" + json.dumps(data))
    logger.debug("UPDATE : 입력받은 파일 수:" + str(len(files)))    
    # 트랜잭션 시작
    keyboardData = KeyboardCreateRequest(**data)    
    delete_file_ids = data['delete_file_ids']
    async with db as session:
        async with session.begin():
            # 1. 지워야 할 첨부파일들 삭제
            for file_id in delete_file_ids:
                # fb_file 테이블에서 파일 정보 삭제
                result = await session.execute(select(FBFile).filter(FBFile.file_id == file_id))
                file_to_delete = result.scalars().first()
                if file_to_delete:
                    # 물리적 파일 삭제
                    file_path = os.path.join(file_to_delete.phy_folder, file_to_delete.phy_name)
                    delete_physical_file(file_path)
                    # fb_file 에서 파일 정보 삭제
                    await session.delete(file_to_delete)
                # file_collection_match 테이블에서 파일 정보 삭제    
                result = await session.execute(select(FileCollectionMatch).filter(FileCollectionMatch.file_id == file_id and FileCollectionMatch.id == keyboard_id))
                fcm_to_delete = result.scalars().first()
                if fcm_to_delete:
                    await session.delete(fcm_to_delete)  
            
            # 2. 추가해야 할 파일들 처리 및 추가
            for file in files:
                # 파일 저장 및 파일 경로, 크기, MIME 타입 받기
                    physical_folder, physical_filename, extension, file_size, mime_type =  await save_upload_file(file)
                    
                    # 파일 메타데이터와 경로를 사용하여 FBFile 인스턴스 생성
                    db_file = FBFile(
                        # file_id=keyboard_id,
                        node_id=keyboard_id,   
                        phy_folder=physical_folder,
                        phy_name=physical_filename,
                        org_name=file.filename,
                        ext=extension,
                        file_size=file_size,
                        mime_type=mime_type,  # 파일의 MIME 타입 추가
                        # 기타 필요한 메타데이터 필드 채우기
                        # create_by=current_user_id  # 현재 사용자 ID로 생성자 정보 추가
                    )
                    session.add(db_file)
                    await session.flush()  # db_file의 file_id를 생성하기 위해 flush 호출

                    # file_collection_match 테이블에 데이터 추가
                    db_fcm = FileCollectionMatch(
                        id=keyboard_id, 
                        file_id=db_file.file_id,
                    )
                    session.add(db_fcm)
                    await session.flush()
            # 3. keyboard 테이블 업데이트
            result = await session.execute(select(KeyboardModel).filter(KeyboardModel.id == keyboard_id))
            keyboard = result.scalars().first()
            if not keyboard:
                session.rollback()
                raise HTTPException(status_code=404, detail="Keyboard not found")
            
            for var, value in vars(keyboardData).items():
                if value is not None:
                    setattr(keyboard, var, value)  # 각 필드 업데이트
            keyboard.create_by = current_user_id
            keyboard.create_on = func.now()  # 수정 시간 업데이트
            await session.commit()
        # 업데이트된 키보드 정보를 바탕으로 KeyboardResponse 생성
        keyboard_response = await get_keyboard_response(session, keyboard_id)
        return keyboard_response            

#
# keyboard 삭제
#
@router.delete("/keyboard/{keyboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyboard(keyboard_id: int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        async with session.begin():
            # keyboard_id에 해당하는 KeyboardModel 검색
            result = await session.execute(select(KeyboardModel).filter(KeyboardModel.id == keyboard_id))
            db_keyboard = result.scalars().first()
            if db_keyboard is None:
                raise HTTPException(status_code=404, detail="Keyboard not found")

            # 해당 keyboard와 연관된 file_collection_match 레코드 찾기
            result = await session.execute(select(FileCollectionMatch).filter(FileCollectionMatch.id == keyboard_id))
            related_file_collection_matches = result.scalars().all()

            # 각 match에 대한 fb_file 찾아서 삭제
            for match in related_file_collection_matches:
                result = await session.execute(select(FBFile).filter(FBFile.file_id == match.file_id))
                related_fb_files = result.scalars().all()
                for fb_file in related_fb_files:
                    # 물리적 파일 삭제
                    file_path = os.path.join(fb_file.phy_folder, fb_file.phy_name)
                    delete_physical_file(file_path)
                    # fb_file 레코드 삭제
                    await session.delete(fb_file)
                # file_collection_match 레코드 삭제
                await session.delete(match)

            # 마지막으로 keyboard 레코드 삭제
            await session.delete(db_keyboard)
            await session.commit()
    return {"ok": True}

async def get_keyboard_response(
    session: AsyncSession, 
    keyboard_id: int
) -> Optional[KeyboardResponse]:
    """업데이트된 키보드 정보와 관련 파일 정보를 조회하여 KeyboardResponse 객체를 생성합니다."""
    updated_keyboard = await session.get(KeyboardModel, keyboard_id)
    if updated_keyboard is None:
        raise HTTPException(status_code=404, detail="Keyboard not found")

    result = await session.execute(select(FBFile).filter(FBFile.file_id == keyboard_id))
    files_info = result.scalars().all()

    files_response = [
        FBFileResponse(
            file_id=file.file_id,
            phy_folder=file.phy_folder,
            phy_name=file.phy_name,
            org_name=file.org_name,
            ext=file.ext,
            file_size=file.file_size,
            mime_type=file.mime_type,
        ) for file in files_info
    ]

    return KeyboardResponse(
        id=updated_keyboard.id,
        product_name=updated_keyboard.product_name,
        manufacturer=updated_keyboard.manufacturer,
        purchase_date=updated_keyboard.purchase_date, #.strftime('%Y-%m-%d'),  # 날짜 포맷 조정
        purchase_amount=updated_keyboard.purchase_amount,
        key_type=updated_keyboard.key_type,
        switch_type=updated_keyboard.switch_type,
        actuation_force=updated_keyboard.actuation_force,
        interface_type=updated_keyboard.interface_type,
        overall_rating=updated_keyboard.overall_rating,
        typing_feeling=updated_keyboard.typing_feeling,
        create_on=updated_keyboard.create_on,
        create_by=updated_keyboard.create_by,
        files=files_response,
        file_count=len(files_response),
    )
