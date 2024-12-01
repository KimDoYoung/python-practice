from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import delete

from app.models.todo_model import Todo
from app.schemas.todo_schema import TodoRequest, TodoResponse

class TodoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_todo(self, todo_id: int) -> TodoResponse:
        """특정 ID로 해야할 일 조회"""
        result = await self.db.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise NoResultFound(f"Todo with ID {todo_id} not found")
        return TodoResponse.from_orm(todo)

    async def get_todos(self) -> list[TodoResponse]:
        """모든 해야할 일 조회"""
        result = await self.db.execute(select(Todo))
        todos = result.scalars().all()
        return [TodoResponse.from_orm(todo) for todo in todos]

    async def create_todo(self, todo_data: TodoRequest) -> TodoResponse:
        """해야할 일 생성"""
        todo = Todo(**todo_data.dict())
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return TodoResponse.from_orm(todo)

    async def update_todo(self, todo_id: int, todo_data: TodoRequest) -> TodoResponse:
        """해야할 일 수정"""
        result = await self.db.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise NoResultFound(f"Todo with ID {todo_id} not found")
        
        for key, value in todo_data.dict(exclude_unset=True).items():
            setattr(todo, key, value)
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        return TodoResponse.from_orm(todo)

    async def delete_todo(self, todo_id: int) -> None:
        """해야할 일 삭제"""
        result = await self.db.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise NoResultFound(f"Todo with ID {todo_id} not found")
        
        await self.db.execute(delete(Todo).where(Todo.id == todo_id))
        await self.db.commit()
