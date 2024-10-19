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
    
    async def get_name(self, category: str, detail_code: str) -> str:
        # sys08_code_kind에서 주어진 category를 찾기 위한 서브쿼리
        subquery = select(Sys08CodeKind.sys08_code_kind_id).filter(Sys08CodeKind.sys08_kind_cd == category).scalar_subquery()

        # sys09_code에서 sys08_code_kind_id와 detail_code로 sys09_name 찾기
        result = await self.db.execute(
            select(Sys09Code.sys09_name).filter(
                Sys09Code.sys09_code_kind_id.in_(subquery),
                Sys09Code.sys09_code == detail_code
            )
        )

        # 첫 번째 결과를 문자열로 반환
        sys09_name = result.scalar()
        return sys09_name if sys09_name else ""