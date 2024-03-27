import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.security import get_current_user
from backend.app.models.keyboard import FBFile, FileCollectionMatch, KeyboardModel
from backend.app.schemas.keyboard_schema import FBFileResponse, KeyboardCreateRequest, KeyboardResponse, KeyboardUpdateRequest, KeyboardRequest
from backend.app.services.keyboard_service import save_upload_file
from backend.app.core.logger import get_logger
from ...services.db_service import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks

logger = get_logger(__name__)

router = APIRouter()

# 리스트 조회
# @router.get("/keyboard", response_model=List[KeyboardResponse])
# async def read_keyboards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     async with db as session:
#         keyboards = await session.execute(select(KeyboardModel).offset(skip).limit(limit))
#         return keyboards.scalars().all()
# @router.get("/keyboard")
# async def read_keyboards(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
#     async with db as session:
#         result = await session.execute(select(KeyboardModel).offset(skip).limit(limit))
#         keyboards = result.scalars().all()
#         keyboard_list = [KeyboardResponse.from_orm(kb).dict() for kb in keyboards]  # ORM 모델을 Pydantic 모델로 변환
#         return JSONResponse(content={"list": keyboard_list, "skip": skip, "limit": limit})
# @router.get("/keyboard")
# async def read_keyboards(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    
#     async with db as session:
#         result = await session.execute(select(KeyboardModel).offset(skip).limit(limit))
#         keyboards = result.scalars().all()
#         keyboard_list = [KeyboardResponse.from_orm(kb) for kb in keyboards]
#         json_compatible_keyboard_list = jsonable_encoder(keyboard_list)
#         return JSONResponse(content={"list": json_compatible_keyboard_list, "skip": skip, "limit": limit})
# @router.get("/keyboard")
# async def read_keyboards(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
#     async with db as session:
#         result = await session.execute(
#             select(
#                 KeyboardModel,
#                 func.count(FileCollectionMatch.file_id).label("file_count")
#             ).join(
#                 FileCollectionMatch, KeyboardModel.id == FileCollectionMatch.id
#             ).group_by(KeyboardModel.id).offset(skip).limit(limit)
#         )
        
#         keyboards = result.all()
#         keyboard_list = [{
#             "keyboard":   KeyboardResponse.from_orm(kb[0]),
#             "file_count": kb[1]
#         } for kb in keyboards]
        
#         json_compatible_keyboard_list = jsonable_encoder(keyboard_list)
#         logger.debug(json_compatible_keyboard_list)
#         return JSONResponse(content={"list": json_compatible_keyboard_list, "skip": skip, "limit": limit})
#
# 조건에 해당하는 리스트 조회
#
@router.get("/keyboard")
async def read_keyboards(skip: int = 0, limit: int = 10, 
                        db: AsyncSession = Depends(get_db),
                        current_user_id: str = Depends(get_current_user),  # JWT 토큰에서 사용자 ID 추출
    ):
    
    async with db as session:
        result = await session.execute(
            select(
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
            .order_by(KeyboardModel.id)
            .offset(skip).limit(limit)
        )
        
        keyboards_info = result.all()
        
        # Transform results into JSON compatible format
        keyboard_list = [
            {
                'id': kb[0], 
                'product_name': kb[1], 
                'manufacturer': kb[2],
                'purchase_date': kb[3],
                'purchase_amount': kb[4],
                'key_type': kb[5],
                'switch_type': kb[6],
                'actuation_force': kb[7],
                'interface_type': kb[8],
                'overall_rating': kb[9],
                'typing_feeling': kb[10],
                'create_on': kb[11],
                'create_by': kb[12],
                "file_count": kb[13] if kb[13] is not None else 0
            } for kb in keyboards_info
        ]
        
        json_compatible_keyboard_list = jsonable_encoder(keyboard_list)
        
        return JSONResponse(content={"list": json_compatible_keyboard_list, "skip": skip, "limit": limit})

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
# @router.get("/keyboard/{keyboard_id}", response_model=KeyboardResponse)
# async def get_keyboard(keyboard_id: int, db: Session = Depends(get_db)):
#     # 키보드 정보 조회
#     keyboard = db.query(KeyboardModel).filter(KeyboardModel.id == keyboard_id).first()
#     if not keyboard:
#         raise HTTPException(status_code=404, detail="Keyboard not found")

#     # 연관된 파일 정보 조회
#     files = db.query(FBFile).filter(FBFile.node_id == keyboard_id).all()
#     files_data = [FBFileResponse(
#         file_id=file.file_id,
#         org_name=file.org_name,
#         mime_type=file.mime_type,
#         file_size=file.file_size,
#         # 추가 정보 필요 시 여기에 포함
#     ) for file in files]

#     return KeyboardResponse(**keyboard.__dict__, files=files_data)

# keyboard DB에 추가
@router.post("/keyboard/insert")
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
                if files:
                    for file in files:
                        # 파일 저장 및 파일 경로, 크기, MIME 타입 받기
                        physical_folder, physical_filename, extension, file_size, mime_type =  save_upload_file(file)
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
                            # 기타 필요한 메타데이터 필드 채우기
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
    return {"message": "Keyboard and files added successfully"}

#
# keyboard 수정
#
@router.put("/keyboard/{keyboard_id}", response_model=KeyboardResponse)
async def update_keyboard(
    keyboard_id: int,
    keyboardData: KeyboardUpdateRequest = Depends(),  # 수정할 필드
#    delete_file_ids: List[int] = Form(default=[]),  # 삭제할 파일 ID
    files: List[UploadFile] = File(default=[]),  # 추가할 파일
    db: AsyncSession = Depends(get_db)
):
    # 트랜잭션 시작
    delete_file_ids = keyboardData.delete_file_ids
    async with db as session:
        async with session.begin():
            # 1. 지워야 할 첨부파일들 삭제
            for file_id in delete_file_ids:
                file_to_delete = db.query(FBFile).filter(FBFile.file_id == file_id).first()
                if file_to_delete:
                    db.delete(file_to_delete)
            
            # 2. 추가해야 할 파일들 처리 및 추가
            for file in files:
                # 파일 저장 및 파일 경로, 크기, MIME 타입 받기
                    physical_folder, physical_filename, extension, file_size, mime_type = await save_upload_file(file)
                    
                    # 파일 메타데이터와 경로를 사용하여 FBFile 인스턴스 생성
                    db_file = FBFile(
                        file_id=keyboard_id,
                        phy_folder=physical_folder,
                        phy_name=physical_filename,
                        ext=extension,
                        file_size=file_size,
                        mime_type=mime_type,  # 파일의 MIME 타입 추가
                        # 기타 필요한 메타데이터 필드 채우기
                        # create_by=current_user_id  # 현재 사용자 ID로 생성자 정보 추가
                    )
                    db.add(db_file)
                    await db.flush()  # db_file의 file_id를 생성하기 위해 flush 호출

                    # file_collection_match 테이블에 데이터 추가
                    db_fcm = FileCollectionMatch(
                        id=keyboard_id, 
                        file_id=db_file.file_id,
                    )
                    db.add(db_fcm)
                
            # 3. keyboard 테이블 업데이트
            keyboard = db.query(KeyboardModel).filter(KeyboardModel.id == keyboard_id).first()
            if not keyboard:
                db.rollback()
                raise HTTPException(status_code=404, detail="Keyboard not found")
            
            for var, value in vars(keyboardData).items():
                if value is not None:
                    setattr(keyboard, var, value)  # 각 필드 업데이트
            
            db.commit()
        
    return {"ok": True}

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
                    await session.delete(fb_file)
                # file_collection_match 레코드 삭제
                await session.delete(match)

            # 마지막으로 keyboard 레코드 삭제
            await session.delete(db_keyboard)
            await session.commit()
    return {"ok": True}
# @router.delete("/keyboard/{keyboard_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_keyboard(keyboard_id: int, db: Session = Depends(get_db)):
#     # 트랜잭션 시작
#     with db.begin():
#         # keyboard_id에 해당하는 KeyboardModel 검색
#         db_keyboard = db.query(KeyboardModel).filter(KeyboardModel.id == keyboard_id).first()
#         if db_keyboard is None:
#             raise HTTPException(status_code=404, detail="Keyboard not found")
        
#         # 해당 keyboard와 연관된 file_collection_match 레코드 찾기
#         related_file_collection_matches = db.query(FileCollectionMatch).filter(FileCollectionMatch.id == keyboard_id).all()
        
#         # 각 match에 대한 fb_file 찾아서 삭제
#         for match in related_file_collection_matches:
#             related_fb_files = db.query(FBFile).filter(FBFile.file_id == match.file_id).all()
#             for fb_file in related_fb_files:
#                 db.delete(fb_file)
#             # file_collection_match 레코드 삭제
#             db.delete(match)
        
#         # 마지막으로 keyboard 레코드 삭제
#         db.delete(db_keyboard)
        
#         # 트랜잭션 커밋은 with 블록 종료 시 자동으로 실행됩니다.

#     return {"ok": True}


