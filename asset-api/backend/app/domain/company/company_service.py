# company_service.py
"""
모듈 설명: 
    - ifi01_company 테이블의 CRUD 서비스
주요 기능:
    - create_company: 회사 정보 생성 (Insert)
    - get_company: 회사 정보 조회 (Read)
    - update_company: 회사 정보 업데이트 (Update)
    - delete_company: 회사 정보 삭제 (Delete)
    - get_company_by_app_key: 회사 정보 조회 By app key

작성자: 김도영
작성일: 2024-10-04
버전: 1.0
"""
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.company.company_model import CompanyModel

# 회사 목록 조회
async def get_all_companies(db: AsyncSession)->List[CompanyModel]:
    ''' 회사 목록 조회 '''
    result = await db.execute(
        select(CompanyModel).order_by(CompanyModel.created_at.desc())
    )
    return result.scalars().all()

# 회사 정보 생성 (Insert)
async def create_company(db: AsyncSession, company_data: dict):
    ''' 회사 정보 생성 insert동작'''
    new_company = CompanyModel(**company_data)
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

# 회사 정보 조회 (Read)
async def get_company(db: AsyncSession, company_id: int, service_nm: str):
    ''' 회사 정보 조회 By company_id, service_nm '''
    result = await db.execute(
        select(CompanyModel).where(CompanyModel.company_id == company_id, CompanyModel.service_nm == service_nm)
    )
    return result.scalar_one_or_none()

# 회사 정보 조회 By app key
async def get_company_by_app_key(db: AsyncSession, app_key: str):
    ''' 회사 정보 조회 By app_key '''
    result = await db.execute(
        select(CompanyModel).where(CompanyModel.app_key == app_key)
    )
    return result.scalar_one_or_none()

# 회사 정보 업데이트 (Update)
async def update_company(db: AsyncSession, company_id: int, service_nm: str, update_data: dict):
    '''  회사 정보 업데이트 (Update) '''
    company = await get_company(db, company_id, service_nm)
    if company:
        for key, value in update_data.items():
            setattr(company, key, value)
        await db.commit()
        await db.refresh(company)
    return company

# 회사 정보 삭제 (Delete)
async def delete_company(db: AsyncSession, company_id: int, service_nm: str):
    '''  회사 정보 삭제 (Delete) '''
    company = await get_company(db, company_id, service_nm)
    if company:
        await db.delete(company)
        await db.commit()
    return company

# async def generate_app_secret_key(company):
#     ''' app_secret_key 생성 '''
#     from backend.app.core.security import aes_encrypt
#     app_key = company.app_key
#     company_id = str(company.company_id)
#     service_nm = company.service_nm
#     start_ymd = company.start_ymd
#     app_secret_key = aes_encrypt(app_key, f"{company_id}|{service_nm}|{start_ymd}")
#     return app_secret_key