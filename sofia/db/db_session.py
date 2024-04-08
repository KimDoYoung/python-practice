
from pathlib import Path

from fastapi import Depends

from db.schema.base_schema import BaseSchema
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated, Generator
from sqlmodel import Session

AsyncSessionLocal = None

def global_init(db_file: str):

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    folder = Path(db_file).parent
    folder.mkdir(parents=True, exist_ok=True)

    async_conn_str = 'sqlite+aiosqlite:///' + db_file.strip()
    print("Connecting to DB with {}".format(async_conn_str))

    engine = create_async_engine(async_conn_str, echo=True, connect_args={"check_same_thread": False})
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # noinspection PyUnresolvedReferences
    import db.schema.__all_schemas

    BaseSchema.metadata.create_all(engine)

def get_db() -> Generator[AsyncSession, None, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# def create_async_session() -> AsyncSession:
#     global __async_engine

#     if not __async_engine:
#         raise Exception("You must call global_init() before using this method.")

#     session: AsyncSession = AsyncSession(__async_engine)
#     session.sync_session.expire_on_commit = False

#     return session

# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with __factory() as session:
#         yield session