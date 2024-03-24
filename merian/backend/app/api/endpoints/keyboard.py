import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.security import get_current_user
from backend.app.models.keyboard import FBFile, FileCollectionMatch, KeyboardModel
from backend.app.schemas.keyboard_schema import KeyboardCreateRequest, KeyboardUpdateRequest, KeyboardRequest
from backend.app.services.keyboard_service import save_upload_file
from ...services.db_service import get_db

router = APIRouter()

@router.get("/keyboard", response_model=List[KeyboardRequest])
async def read_keyboards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    keyboards = db.query(KeyboardModel).offset(skip).limit(limit).all()
    return keyboards

@router.post("/keyboard/insert")
async def create_keyboard(keyboardData: str = Form(...), 
                files: List[UploadFile] = File(...), 
                db: Session = Depends(get_db),
                current_user_id: str = Depends(get_current_user)  # JWT 토큰에서 사용자 ID 추출
            ):
    data = json.loads(keyboardData)
    keyboard_request = KeyboardCreateRequest(**data)

    async with db.begin() as transaction:  # 트랜잭션 시작
        try:
            # KeyboardModel 인스턴스 생성 및 삽입
            keyboard_db = KeyboardModel(keyboard_request)
            db.add(keyboard_db)
            await transaction.commit()  # 트랜잭션 커밋으로 데이터베이스에 반영

            for file in files:
                # 파일 저장 및 파일 경로, 크기, MIME 타입 받기
                physical_folder, physical_filename, extension, file_size, mime_type = await save_upload_file(file)
                
                # 파일 메타데이터와 경로를 사용하여 FBFile 인스턴스 생성
                db_file = FBFile(
                    file_id=keyboard_db.id,
                    phy_folder=physical_folder,
                    phy_name=physical_filename,
                    ext=extension,
                    file_size=file_size,
                    mime_type=mime_type,  # 파일의 MIME 타입 추가
                    # 기타 필요한 메타데이터 필드 채우기
                    create_by=current_user_id  # 현재 사용자 ID로 생성자 정보 추가
                )
                db.add(db_file)
                await db.flush()  # db_file의 file_id를 생성하기 위해 flush 호출

                # file_collection_match 테이블에 데이터 추가
                db_fcm = FileCollectionMatch(
                    id=keyboard_db.id,
                    file_id=db_file.file_id,
                )
                db.add(db_fcm)

            await transaction.commit()  # 최종 커밋
        except Exception as e:
            await transaction.rollback()  # 오류 발생 시 롤백
            raise e
    return {"message": "Keyboard and files added successfully"}

# @router.post("/keyboard/insert", response_model=KeyboardRequest)
# async def create_keyboard( keyboardData: str = Form(...),  files: List[UploadFile] = File(...),db: Session = Depends(get_db)):

#     data = json.loads(keyboardData) # JSON 문자열을 파이썬 객체로 파싱
#     keyboard_data = KeyboardCreateRequest(**data)
    
#     # 트랜잭션 시작
#     transaction = db.begin()
#     try:
#         data = json.loads(keyboardData)
#         keyboard_data = KeyboardCreateRequest(**data)
        
#         # KeyboardModel 인스턴스 생성 및 삽입
#         db_keyboard = KeyboardModel( keyboard_data )
#         db.add(db_keyboard)
#         db.commit()
#         for file in files:
#             # 파일 처리 및 FBFile 인스턴스 생성
#             contents = await file.read() # 예시, 실제로는 파일을 저장해야 함
#             db_file = FBFile(
#                 node_id=db_keyboard.id, # 예시, 실제 node_id 구조에 맞게 조정
#                 # 기타 필드 채우기
#             )
#             db.add(db_file)
        
#         # 모든 작업이 성공적으로 완료되면 커밋
#         db.commit()
#     except Exception as e:
#         db.rollback() # 오류 발생 시 롤백
#         raise e

#     # SQLAlchemy 모델 인스턴스 생성
#     db_keyboard = KeyboardModel(**keyboard_data)
#     db.add(db_keyboard)
#     db.commit()
#     db.refresh(db_keyboard)

#     for file in files:
#         # 각 파일 처리
#         contents = await file.read()

#     return db_keyboard

@router.delete("/keyboard/{keyboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyboard(keyboard_id: int, db: Session = Depends(get_db)):
    db_keyboard = db.query(KeyboardRequest).filter(KeyboardRequest.id == keyboard_id).first()
    if db_keyboard is None:
        raise HTTPException(status_code=404, detail="Keyboard not found")
    db.delete(db_keyboard)
    db.commit()
    return {"ok": True}

@router.put("/keyboard/{keyboard_id}", response_model=KeyboardRequest)
async def update_keyboard(keyboard_id: int, keyboard: KeyboardUpdateRequest, db: Session = Depends(get_db)):
    db_keyboard = db.query(KeyboardRequest).filter(KeyboardRequest.id == keyboard_id).first()
    if db_keyboard is None:
        raise HTTPException(status_code=404, detail="Keyboard not found")
    for var, value in vars(keyboard).items():
        setattr(db_keyboard, var, value) if value else None
    db.commit()
    db.refresh(db_keyboard)
    return db_keyboard
