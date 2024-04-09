from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from core.logger import get_logger

logger = get_logger(__name__)
# 여기서 AsyncSessionLocal을 전역 변수로 선언

db_file = (Path(__file__).resolve().parent.parent / "data" / "sofia.sqlite").absolute()

DB_URL= 'sqlite+aiosqlite:///' + str(db_file).strip() #"sqlite+aiosqlite:///C:/Users/deHong/Documents/kdy/python-practice/sofia/data/sofia.sqlite"
logger.debug("----> DB_URL: " + DB_URL)
engine = create_async_engine(DB_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
logger.debug("----> AsyncSessionLocal created.")


#async def global_init(db_file: str):
async def global_init():
    global AsyncSessionLocal

    # if not db_file or not db_file.strip():
    #     raise Exception("You must specify a db file.")

    try:
        # folder = Path(db_file).parent
        # folder.mkdir(parents=True, exist_ok=True)

        # async_conn_str = 'sqlite+aiosqlite:///' + db_file.strip()
        # print(f"Connecting to DB with {async_conn_str}")

        # engine = create_async_engine(async_conn_str, echo=True, future=True)
        # AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        # logger.debug("----> AsyncSessionLocal created.")
        # if AsyncSessionLocal is None:
        #     raise Exception("AsyncSessionLocal is None.")
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("====> Database tables created.")
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
        raise
