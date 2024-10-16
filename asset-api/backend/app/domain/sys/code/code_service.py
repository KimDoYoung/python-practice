
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.sys.code.sys08_09_model import Sys08CodeKind, Sys09Code

class CodeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_code_by_category(self, category: str):
        '''하위 쿼리: sys08_code_kind 테이블에서 예를들어 sys08_kind_cd가 'ApiServiceCode'인 sys08_code_kind_id 선택'''
        subquery = select(Sys08CodeKind.sys08_code_kind_id).where(Sys08CodeKind.sys08_kind_cd == category)

        # 메인 쿼리: sys09_code 테이블에서 sys09_code_kind_id가 하위 쿼리 결과에 있는 항목을 찾고, sys09_seq로 정렬
        result = self.db.query(Sys09Code).filter(Sys09Code.sys09_code_kind_id.in_(subquery)).order_by(Sys09Code.sys09_seq).all()

        return result