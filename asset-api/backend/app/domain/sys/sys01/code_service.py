from sqlalchemy.future import select  
from backend.app.domain.sys.sys01.sys01_company_model import Sys09Code, Sys08CodeKind
from backend.app.core.database import get_session

class CodeService:

    @staticmethod
    async def get_code_by_category(category: str) -> list[Sys09Code]:
        """주어진 카테고리의 코드 목록을 sys09_seq 순서로 가져옵니다."""
        async with get_session() as session:
            # 카테고리에 해당하는 code_kind_id 조회를 위한 하위 쿼리
            subquery = select(Sys08CodeKind.sys08_code_kind_id).where(Sys08CodeKind.sys08_kind_cd == category)

            # 메인 쿼리: sys09_code_kind_id가 하위 쿼리 결과에 있는 코드 목록 조회
            query = (
                select(Sys09Code)
                .where(Sys09Code.sys09_code_kind_id.in_(subquery))
                .order_by(Sys09Code.sys09_seq)
            )

            result = await session.execute(query)
            codes = result.scalars().all()
            return codes

    @staticmethod
    async def get_name(category: str, detail_code: str) -> str:
        """주어진 카테고리와 상세 코드에 맞는 sys09_name을 반환합니다."""
        async with get_session() as session:
            # 카테고리에 해당하는 code_kind_id 조회를 위한 하위 쿼리
            subquery = select(Sys08CodeKind.sys08_code_kind_id).where(Sys08CodeKind.sys08_kind_cd == category).scalar_subquery()

            # 메인 쿼리: sys09_code_kind_id가 하위 쿼리 결과에 있고, detail_code에 맞는 코드의 이름 조회
            query = select(Sys09Code.sys09_name).where(
                Sys09Code.sys09_code_kind_id.in_(subquery),
                Sys09Code.sys09_code == detail_code
            )

            result = await session.execute(query)
            sys09_name = result.scalar()
            return sys09_name or ""
