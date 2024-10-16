from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.ifi.ifi10.ifi10_law_model import Ifi10Law
from backend.app.domain.ifi.ifi10.ifi10_law_schema import Ifi10LawResponse
from backend.app.domain.service.law.law_schema import Law010_Request, Law010_Response

class LawService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
async def run_r010(self, req: Law010_Request) -> Law010_Response:
    
    start_idx = req.conti_start_idx
    limit = req.conti_limit
    conti_yn = req.conti_yn # 연속 조회 여부 쓸데가 없네.
    # limit + 1개만큼 조회해서 추가 데이터 존재 여부 확인 (exists_yn)
    stmt = (
        select(Ifi10Law)
        .order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)  # 정렬 조건
        .offset(start_idx)  # 시작 인덱스
        .limit(limit + 1)  # limit + 1개의 데이터 조회
    )

    # 비동기 쿼리 실행
    result = await self.db.execute(stmt)
    rows = result.scalars().all()

    # Law010_Response를 위한 기본 설정
    law_response = Law010_Response(
        msg_cd="0000",  # 성공 코드
        msg="Success"
    )

    # 데이터가 limit + 1개로 조회되었다면 추가 데이터가 존재함 (exists_yn = "Y")
    if len(rows) > limit:
        law_response.exists_yn = "Y"
        rows = rows[:limit]  # limit 만큼만 데이터 자르기
    else:
        law_response.exists_yn = "N"

    # 조회된 데이터가 있는 경우, 마지막 인덱스를 conti_last_idx로 설정
    if rows:
        law_response.conti_last_idx = start_idx + len(rows) - 1

    # 조회된 데이터를 Ifi10LawResponse로 변환하여 output에 추가
    law_response.output = [Ifi10LawResponse(**row.__dict__) for row in rows]

    # count는 조회된 데이터의 개수로 설정 (limit 개수에 해당하는 값)
    law_response.count = len(law_response.output)

    return law_response
