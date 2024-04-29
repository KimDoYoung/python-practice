from fastapi import APIRouter, Depends, HTTPException, Body, Path
from app.core.dependency import get_user_service
from app.domain.users.user_model import User
from app.domain.users.user_service import UserService

# APIRouter 인스턴스 생성
user_router = APIRouter()

@user_router.get("/users", response_model=list[User])
async def get_all_users(user_service :UserService=Depends(get_user_service)):
    users = await user_service.get_all_users()
    return users

@user_router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: str = Path(...), user_service :UserService=Depends(get_user_service)):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/user", response_model=User)
async def create_user(user_data: User = Body(...), user_service :UserService=Depends(get_user_service)):
    user = await user_service.create_user(user_data.dict())
    return user

@user_router.put("/user/{user_id}", response_model=User)
async def update_user(user_id: str = Path(...), update_data: dict = Body(...), user_service :UserService=Depends(get_user_service)):
    user = await user_service.update_user(user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: str = Path(...), user_service :UserService=Depends(get_user_service)):
    await user_service.delete_user(user_id)
    return {"msg": f"User {user_id} deleted successfully"}
