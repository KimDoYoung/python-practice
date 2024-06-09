from fastapi import APIRouter, Depends, HTTPException, Body, Path
from backend.app.core.dependency import get_user_service
from backend.app.domains.user.user_model import User
from backend.app.domains.user.user_service import UserService

# APIRouter 인스턴스 생성
router = APIRouter()

# @router.get("/users", response_model=list[User])
# async def get_all_users(user_service :UserService=Depends(get_user_service)):
#     users = await user_service.get_all_users()
#     return users
#TODO : 사용자 정보 특히 key를 수정 추가할 수 있어야한다.
#TODO : 처음에 어떻게 할 것인가? admin이 있어서 사용자를 추가할 것인가? 아니면 사용자가 직접 추가할 것인가?
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, user_service :UserService=Depends(get_user_service)):
    user = await user_service.get_1(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str = Path(...), update_data: dict = Body(...), user_service :UserService=Depends(get_user_service)):
    user = await user_service.update_user(user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
