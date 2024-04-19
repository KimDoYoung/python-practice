from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.logger import get_logger

logger = get_logger(__name__)



DATABASE_URL = "postgresql+asyncpg://kdy987:kalpa987!@localhost/stock"
logger.debug("----> DATABASE_URL: " + DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
logger.debug("----> AsyncSessionLocal created.")

