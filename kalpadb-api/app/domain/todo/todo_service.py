from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from app.domain.todo.todo_model import Todo
from app.domain.todo.todo_schema import TodoResponse, TodoCreateRequest

class TodoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_todos(self) -> list[TodoResponse]:
        """모든 해야할 일 조회"""
        query = (
                select(Todo)
                .where(Todo.done_yn == "N")  # 조건: 완료되지 않은 항목
                .order_by(desc(Todo.input_dt))  # 입력일 기준 내림차순 정렬
            )

        result = await self.db.execute(query)
        todos =  result.scalars().all()
        return [TodoResponse.model_validate(todo.__dict__) for todo in todos]

    async def create_todo(self, req: TodoCreateRequest) -> bool:
        """해야할 일 생성"""

        # 각 todo 항목을 데이터베이스에 추가
        for todo_content in req.todos:
            todo = Todo(content=todo_content)  # Todo 객체 생성
            self.db.add(todo)

        # 변경 사항 저장
        await self.db.commit()
        return True

    async def set_todo_done(self, id: int) -> bool:
        """해야할 일 완료 처리"""
        query = (
            select(Todo)
            .where(Todo.id == id)
        )

        result = await self.db.execute(query)
        todo = result.scalars().first()
        if todo:
            todo.done_yn = "Y"
            todo.done_dt = datetime.now()
            await self.db.commit()
            return True
        return False