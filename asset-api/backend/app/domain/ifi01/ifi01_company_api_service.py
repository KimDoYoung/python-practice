from typing import List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.domain.ifi01.ifi01_company_api_model import Ifi01CompanyApi
from backend.app.domain.ifi01.ifi01_company_api_schema import Ifi01CompanyApiCreate

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

        # 새로운 Ifi01CompanyApi 객체 생성
        new_company_api = Ifi01CompanyApi(
            ifi01_company_api_id = company_api_id,
            ifi01_company_id = data['ifi01_company_id'],
            ifi01_config_api_id = data['ifi01_config_api_id'],
            ifi01_start_date = data['ifi01_start_date'],
            ifi01_close_date = data['ifi01_close_date'],
            ifi01_app_key = data['ifi01_app_key']
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
    async def delete_company_api(self, company_api_id: int):
        ''' 회사 API 삭제 '''
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
        result = await self.db.execute(stmt)
        deleted_company = result.scalar_one_or_none()
        self.db.delete(deleted_company)
        await self.db.commit()
        return deleted_company
    
    # 회사 API 정보 업데이트
    async def update_company_api(self, company_api_id: int, company_api_data: Ifi01CompanyApiCreate):
        ''' 회사 API 정보 업데이트 '''
        stmt = select(Ifi01CompanyApi).where(Ifi01CompanyApi.ifi01_company_api_id == company_api_id)
        result = await self.db.execute(stmt)
        updated_company = result.scalar_one_or_none()
        updated_company.update(company_api_data.model_dump(exclude_unset=True))
        await self.db.commit()
        return updated_company