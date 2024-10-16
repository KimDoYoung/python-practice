from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi95.ifi95_config_file_model import Ifi95ConfigFile
from backend.app.domain.ifi.ifi95.ifi95_config_file_schema import Ifi95ConfigFileCreate

class Ifi95ConfigFileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 파일 송수신 설정 생성
    async def create_config_file(self, config_file_data: Ifi95ConfigFileCreate):
        new_config_file = Ifi95ConfigFile(**config_file_data.dict())
        self.db.add(new_config_file)
        await self.db.commit()
        await self.db.refresh(new_config_file)
        return new_config_file

    # 파일 송수신 설정 정보 가져오기
    async def get_config_file(self, config_file_id: int):
        stmt = select(Ifi95ConfigFile).where(Ifi95ConfigFile.ifi95_config_file_id == config_file_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 파일 송수신 설정 리스트 가져오기
    async def get_config_files(self):
        stmt = select(Ifi95ConfigFile)
        result = await self.db.execute(stmt)
        return result.scalars().all()
