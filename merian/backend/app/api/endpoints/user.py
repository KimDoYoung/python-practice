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


router = APIRouter()

class LoginFormData(BaseModel):
    username: str
    password: str
    
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: LoginFormData, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "name" : user.nm}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.id == username).first()
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user
