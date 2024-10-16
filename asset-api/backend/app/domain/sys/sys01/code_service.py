from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select
from backend.app.domain.sys.sys01.sys01_company_model import Sys09Code, Sys08CodeKind

class CodeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_code_by_category(self, category: str) -> list[Sys09Code]:
        '''하위 쿼리: sys08_code_kind 테이블에서 예를들어 sys08_kind_cd가 'ApiServiceCode'인 sys08_code_kind_id 선택'''
        subquery = select(Sys08CodeKind.sys08_code_kind_id).where(Sys08CodeKind.sys08_kind_cd == category)

        # 메인 쿼리: sys09_code 테이블에서 sys09_code_kind_id가 하위 쿼리 결과에 있는 항목을 찾고, sys09_seq로 정렬
        query = select(Sys09Code).where(Sys09Code.sys09_code_kind_id.in_(subquery)).order_by(Sys09Code.sys09_seq)

        # AsyncSession을 사용해 쿼리 실행 및 결과 반환
        result = await self.db.execute(query)
        
        # 결과에서 스칼라 값을 추출하여 리스트로 변환
        codes = result.scalars().all()

        return codes
