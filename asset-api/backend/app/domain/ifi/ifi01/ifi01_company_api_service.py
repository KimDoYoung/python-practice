from datetime import datetime
from typing import List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi.ifi01.ifi01_company_api_model import Ifi01CompanyApi
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class Ifi01CompanyApiService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Database에서 ifi01_company_api_id를 생성하는 함수 호출
    async def generate_company_api_id(self):
        query = text("SELECT f_create_seq()")  # DB 함수 호출
        result = await self.db.execute(query)
        return result.scalar()

    # 회사 API 정보를 생성하는 함수
    async def create_company_api(self, data: dict):
        # ifi01_company_api_id를 데이터베이스 함수에서 가져옴
        company_api_id = await self.generate_company_api_id()

        # 만약 ifi01_start_date와 ifi01_close_date가 문자열로 들어오면 변환
        if isinstance(data['ifi01_start_date'], str):
            ifi01_start_date = datetime.strptime(data['ifi01_start_date'], '%Y-%m-%d').date()
        else:
            ifi01_start_date = data['ifi01_start_date']  # 이미 date 객체라면 그대로 사용

        if isinstance(data['ifi01_close_date'], str):
            ifi01_close_date = datetime.strptime(data['ifi01_close_date'], '%Y-%m-%d').date()
        else:
            ifi01_close_date = data['ifi01_close_date']  # 이미 date 객체라면 그대로 사용

        current_time = datetime.now() # timestamp with time zone
        # 새로운 Ifi01CompanyApi 객체 생성
        new_company_api = Ifi01CompanyApi(
            ifi01_company_api_id = company_api_id,
            ifi01_company_id = data['ifi01_company_id'],
            ifi01_config_api_id = data['ifi01_config_api_id'],
            ifi01_start_date = data['ifi01_start_date'],
            ifi01_close_date = data['ifi01_close_date'],
            ifi01_app_key = data['ifi01_app_key'],
            ifi01_created_date = current_time,
        )
        
        # 데이터베이스에 저장
        self.db.add(new_company_api)
        await self.db.commit()
        await self.db.refresh(new_company_api)
        return new_company_api
    
    # 회사 API 정보를 app_key로 찾아오는 함수
    async def get_company_by_app_key(self, app_key: str) -> Ifi01CompanyApi:
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_app_key == app_key)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() # 결과가 없으면 None 반환

    # 회사 API 정보 가져오기
    async def get_company_api(self, company_api_id: int) -> Ifi01CompanyApi:
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # 회사 API 리스트 가져오기
    async def get_company_all(self)->List[Ifi01CompanyApi]:
        '''모든 회사 API 리스트 가져오기 입력날짜의 역순으로 가져온다'''
        stmt = select(Ifi01CompanyApi).order_by(Ifi01CompanyApi.ifi01_created_date.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    # 회사 API 삭제
    # async def delete_company_api(self, company_api_id: int):
    #     ''' 회사 API 삭제 '''
    #     stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
    #     result = await self.db.execute(stmt)
    #     deleted_company = result.scalar_one_or_none()
    #     self.db.delete(deleted_company)
    #     await self.db.commit()
    #     return deleted_company
    async def delete_company_api(self, company_api_id: int):
        ''' 회사 API 삭제 '''
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
        result = await self.db.execute(stmt)
        deleted_company = result.scalar_one_or_none()

        if deleted_company is None:
            logger.error(f"Company API with id {company_api_id} not found.")
            raise ValueError(f"Company API with id {company_api_id} does not exist.")
        
        try:
            await self.db.delete(deleted_company)
            # await self.db.flush()  # flush 호출
            await self.db.commit()  # 커밋 시도
            logger.info(f"Company API with id {company_api_id} successfully deleted.")
        except Exception as e:
            logger.error(f"Failed to delete Company API with id {company_api_id}: {e}")
            await self.db.rollback()  # 커밋 실패 시 롤백
            raise ValueError(f"Failed to delete Company API with id {company_api_id}: {str(e)}")

        return deleted_company
        
    
    # 회사 API 정보 업데이트
    async def update_company_api(self, company_api_id: int, data_dict: dict):
        ''' 회사 API 정보 업데이트 '''
        # 레코드 조회
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
        result = await self.db.execute(stmt)
        updated_company = result.scalar_one_or_none()
        
        # 객체가 존재하는지 확인
        if updated_company is None:
            raise ValueError(f"Company API with id {company_api_id} not found.")
        
        # 각 필드에 값을 할당 (data_dict에 있는 값으로)
        for key, value in data_dict.items():
            if hasattr(updated_company, key):  # updated_company에 해당 속성이 있으면
                setattr(updated_company, key, value)
        
        # 변경사항 커밋
        await self.db.commit()
        
        return updated_company