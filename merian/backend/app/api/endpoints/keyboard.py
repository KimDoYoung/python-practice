from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from ...services.db_utils import get_db
from ...models.keyboard import Keyboard  # Keyboard 모델 정의를 가정
from ...schemas.keyboard import KeyboardCreate, KeyboardUpdate  # Keyboard 스키마 정의를 가정

router = APIRouter()

@router.get("/keyboard/", response_model=List[Keyboard])
async def read_keyboards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    keyboards = db.query(Keyboard).offset(skip).limit(limit).all()
    return keyboards

@router.post("/keyboard/insert", response_model=Keyboard)
async def create_keyboard(keyboard: KeyboardCreate, db: Session = Depends(get_db)):
    db_keyboard = Keyboard(**keyboard.dict())
    db.add(db_keyboard)
    db.commit()
    db.refresh(db_keyboard)
    return db_keyboard

@router.delete("/keyboard/{keyboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyboard(keyboard_id: int, db: Session = Depends(get_db)):
    db_keyboard = db.query(Keyboard).filter(Keyboard.id == keyboard_id).first()
    if db_keyboard is None:
        raise HTTPException(status_code=404, detail="Keyboard not found")
    db.delete(db_keyboard)
    db.commit()
    return {"ok": True}

@router.put("/keyboard/{keyboard_id}", response_model=Keyboard)
async def update_keyboard(keyboard_id: int, keyboard: KeyboardUpdate, db: Session = Depends(get_db)):
    db_keyboard = db.query(Keyboard).filter(Keyboard.id == keyboard_id).first()
    if db_keyboard is None:
        raise HTTPException(status_code=404, detail="Keyboard not found")
    for var, value in vars(keyboard).items():
        setattr(db_keyboard, var, value) if value else None
    db.commit()
    db.refresh(db_keyboard)
    return db_keyboard
