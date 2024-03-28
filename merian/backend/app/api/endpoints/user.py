from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.configs import ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.services.db_service import get_db

from ...core.security import create_access_token, verify_password
from ...schemas.user_schema import Token
from ...models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter()

class LoginFormData(BaseModel):
    username: str
    password: str
    
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginFormData, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "name": user.nm}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 사용자 인증 함수 - 비동기 함수로 변경
async def authenticate_user(db: AsyncSession, username: str, password: str):
    async with db as session:
        user = await session.execute(select(User).filter(User.id == username))
        user = user.scalars().first()
        if user and user.verify_password(password):
            return user
    return False