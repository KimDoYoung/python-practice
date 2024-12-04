from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.domain.todo.todo_schema import TodoCreateRequest, TodoResponse
from app.domain.todo.todo_service import TodoService


router = APIRouter()

@router.post("/todo", response_model=dict)
async def insert_todos(
    req: TodoCreateRequest,
    db: AsyncSession = Depends(get_session)
):
    ''' 할일 목록 생성 '''
    service = TodoService(db)
    b = await service.create_todo(req)
    if b:
        return {"result": "success"}
    return {"result": "fail"}

@router.get("/todo", response_model=List[TodoResponse])
async def get_todos(db: AsyncSession = Depends(get_session)):
    ''' 해야 할일 목록 리스트 '''
    service = TodoService(db)
    return await service.get_todos()

@router.put("/todo/{id}", response_model=List[TodoResponse])
async def get_todos(id:int, db: AsyncSession = Depends(get_session)):
    ''' 해야 할 일 완료처리 및 리스트 '''
    service = TodoService(db)
    b = await service.set_todo_done(id)
    if b:
        return await service.get_todos()
    else:
        raise HTTPException(status_code=404, detail="Item not found")
