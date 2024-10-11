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
from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException
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
    
    # select 구문에서 new_company 대신 CompanyModel 클래스를 사용합니다.
    existing_company = await db.execute(
        select(CompanyModel).where(
            CompanyModel.company_id == company_data['company_id'],
            CompanyModel.service_id == company_data['service_id']
        )
    )
    
    # 기존 회사가 존재하는지 확인
    existing_company = existing_company.scalar()  # `first()` 대신 `scalar()` 사용하여 첫 번째 값을 가져옴
    
    if existing_company:
        raise HTTPException(status_code=400, detail="Company already exists with the same company_id and service_id")    
    
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

# 회사 정보 조회 (Read)
async def get_company(db: AsyncSession, company_id: int, service_id: str):
    ''' 회사 정보 조회 By company_id, service_id '''
    result = await db.execute(
        select(CompanyModel).where(CompanyModel.company_id == company_id, CompanyModel.service_id == service_id)
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
async def update_company(db: AsyncSession, company_id: int, service_id: str, update_data: dict):
    '''  회사 정보 업데이트 (Update) '''
    company = await get_company(db, company_id, service_id)
    if company:
        for key, value in update_data.items():
            setattr(company, key, value)
        company.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(company)
    return company

# 회사 정보 삭제 (Delete)
async def delete_company(db: AsyncSession, company_id: int, service_id: str):
    '''  회사 정보 삭제 (Delete) '''
    company = await get_company(db, company_id, service_id)
    if company:
        await db.delete(company)
        await db.commit()
    return company

