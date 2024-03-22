import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session
from typing import List

from backend.app.models.keyboard import FBFile, KeyboardModel
from backend.app.schemas.keyboard_schema import KeyboardCreateRequest, KeyboardUpdateRequest, KeyboardRequest
from ...services.db_service import get_db

router = APIRouter()

@router.get("/keyboard", response_model=List[KeyboardRequest])
async def read_keyboards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    keyboards = db.query(KeyboardModel).offset(skip).limit(limit).all()
    return keyboards

@router.post("/keyboard/insert", response_model=KeyboardRequest)
async def create_keyboard( keyboardData: str = Form(...),  files: List[UploadFile] = File(...),db: Session = Depends(get_db)):

    data = json.loads(keyboardData) # JSON 문자열을 파이썬 객체로 파싱
    keyboard_data = KeyboardCreateRequest(**data)
    
    # 트랜잭션 시작
    transaction = db.begin()
    try:
        data = json.loads(keyboardData)
        keyboard_data = KeyboardCreateRequest(**data)
        
        # KeyboardModel 인스턴스 생성 및 삽입
        db_keyboard = KeyboardModel( keyboard_data )
        db.add(db_keyboard)
        db.commit()
        for file in files:
            # 파일 처리 및 FBFile 인스턴스 생성
            contents = await file.read() # 예시, 실제로는 파일을 저장해야 함
            db_file = FBFile(
                node_id=db_keyboard.id, # 예시, 실제 node_id 구조에 맞게 조정
                # 기타 필드 채우기
            )
            db.add(db_file)
        
        # 모든 작업이 성공적으로 완료되면 커밋
        db.commit()
    except Exception as e:
        db.rollback() # 오류 발생 시 롤백
        raise e

    # SQLAlchemy 모델 인스턴스 생성
    db_keyboard = KeyboardModel(**keyboard_data)
    db.add(db_keyboard)
    db.commit()
    db.refresh(db_keyboard)

    for file in files:
        # 각 파일 처리
        contents = await file.read()

    return db_keyboard

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
