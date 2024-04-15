from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from core.logger import get_logger

logger = get_logger(__name__)


db_file = (Path(__file__).resolve().parent.parent / "data" / "sofia.sqlite").absolute()
# 폴더가 없으면 만든다.
folder = db_file.parent
folder.mkdir(parents=True, exist_ok=True)

DB_URL= 'sqlite+aiosqlite:///' + str(db_file).strip() 
logger.debug("----> DB_URL: " + DB_URL)
engine = create_async_engine(DB_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
logger.debug("----> AsyncSessionLocal created.")


# 데이터베이스를 초기화하는 함수이다.
async def global_init():
    global AsyncSessionLocal

    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("====> Database tables created.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
        raise
