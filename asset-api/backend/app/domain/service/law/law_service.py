from sqlalchemy import func, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.domain.ifi.ifi10.ifi10_law_model import Ifi10Law
from backend.app.domain.ifi.ifi10.ifi10_law_schema import Ifi10Law_Response
from backend.app.domain.ifi.ifi11.ifi11_law_record_model import Ifi11LawRecord
from backend.app.domain.ifi.ifi92.ifi92_api_layout_model import Ifi92ApiLayout
from backend.app.domain.service.law.law_schema import Law010_Request, Law010_Response, Law011_Request

class LawService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_r010_all(self, req: Law010_Request) -> Law010_Response:
        ''' r010 법큐정보 조회 (전체) '''
        stmt = (
            select(Ifi10Law)
            .order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)  # 정렬 조건
        )

        # 비동기 쿼리 실행
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        # Law010_Response를 위한 기본 설정
        law_response = Law010_Response(
            msg_cd="00",  # 성공 코드
            msg="Success"
        )
        # 나머지 데이터는 없음
        law_response.exists_yn = "N"

        if rows:
            law_response.conti_last_idx =  len(rows) - 1

        # 조회된 데이터를 Ifi10Law_Response로 변환하여 output에 추가
        law_response.output = [Ifi10Law_Response(**row.__dict__) for row in rows]

        # count는 조회된 데이터의 개수로 설정 (limit 개수에 해당하는 값)
        law_response.count = len(law_response.output)

        return law_response        
    
    async def run_r010_paging(self, req: Law010_Request) -> Law010_Response:
        ''' r010 법큐정보 조회 (페이징) '''
        start_idx = req.conti_start_idx
        limit = req.conti_limit
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
            msg_cd="00",  # 성공 코드
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

        # 조회된 데이터를 Ifi10Law_Response로 변환하여 output에 추가
        law_response.output = [Ifi10Law_Response(**row.__dict__) for row in rows]

        # count는 조회된 데이터의 개수로 설정 (limit 개수에 해당하는 값)
        law_response.count = len(law_response.output)

        return law_response     

    async def run_r010(self, req: Law010_Request) -> Law010_Response:
        ''' r010 법큐정보 조회'''
        if req.all_yn == "Y":
            return await self.run_r010_all(req)
        else:
            return await self.run_r010_paging(req) 


    async def field_mapping(self, layout_cd: str):
        ''' law10에서 필드 매핑 정보 추출 
        SELECT 
            RIGHT(ifi92_element_nm, length(ifi92_element_nm) - 1) AS ifi92_element_nm
            , ifi92_link_column 
        FROM 
            ifi92_api_layout 
        WHERE ifi92_layout_cd='LAW010'
            AND ifi92_message_cd='RES'
            AND ifi92_component_cd = 'B'
            AND ifi92_link_column IS NOT null	
        ORDER BY ifi92_seq;
        '''
        stmt = (
            select(func.substr( Ifi92ApiLayout.ifi92_element_nm, 2).label('ifi92_element_nm') , Ifi92ApiLayout.ifi92_link_column)
            .where(
                Ifi92ApiLayout.ifi92_layout_cd == layout_cd,
                Ifi92ApiLayout.ifi92_message_cd == 'RES',
                Ifi92ApiLayout.ifi92_component_cd == 'B',
                Ifi92ApiLayout.ifi92_link_column.isnot(None)  # link_column이 NULL이 아닌 값
            )
            .order_by(Ifi92ApiLayout.ifi92_seq)  # 순서대로 정렬
        )

        # 비동기 쿼리 실행
        result = await self.db.execute(stmt)
        rows = result.fetchall()

        # field_mapping 생성
        field_mapping = {row.ifi92_element_nm: row.ifi92_link_column for row in rows}

        return field_mapping

    async def run_r011_all(self, req: Law011_Request) -> Law010_Response:
        subquery = (
            select(Ifi11LawRecord.ifi11_class_tree_cd, Ifi11LawRecord.ifi11_deadline_id)
            .where(
                Ifi11LawRecord.ifi11_dml_type.notin_(['DELETE']),
                Ifi11LawRecord.ifi11_dml_date.between(func.to_date('20241001', 'YYYYMMDD'), func.to_date('20241101', 'YYYYMMDD'))
            )
            .subquery()
        )

        # 메인 쿼리: ifi10_law 테이블에서 서브쿼리 결과와 매칭되는 데이터 조회
        stmt = (
            select(Ifi10Law)
            .where(
                tuple_(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id).in_(subquery)
            ).order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)  # 정렬 조건
        )

        # 비동기 쿼리 실행
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        law_response = Law010_Response(
            msg_cd="00",  # 성공 코드
            msg="Success"
        )
        # 나머지 데이터는 없음
        law_response.exists_yn = "N"

        if rows:
            law_response.conti_last_idx =  len(rows) - 1

        # 조회된 데이터를 Ifi10Law_Response로 변환하여 output에 추가
        law_response.output = [Ifi10Law_Response(**row.__dict__) for row in rows]

        # count는 조회된 데이터의 개수로 설정 (limit 개수에 해당하는 값)
        law_response.count = len(law_response.output)

        return law_response          
    
    async def run_r011_paging(self, req: Law011_Request) -> Law010_Response:
        start_idx = req.conti_start_idx
        limit = req.conti_limit
        subquery = (
            select(Ifi11LawRecord.ifi11_class_tree_cd, Ifi11LawRecord.ifi11_deadline_id)
            .where(
                Ifi11LawRecord.ifi11_dml_type.notin_(['DELETE']),
                Ifi11LawRecord.ifi11_dml_date.between(func.to_date('20241001', 'YYYYMMDD'), func.to_date('20241101', 'YYYYMMDD'))
            )
            .subquery()
        )

        # 메인 쿼리: ifi10_law 테이블에서 서브쿼리 결과와 매칭되는 데이터 조회
        stmt = (
            select(Ifi10Law)
            .where(
                tuple_(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id).in_(subquery)
            )
            .order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)  # 정렬 조건
            .offset(start_idx)  # 시작 인덱스
            .limit(limit + 1)  # limit + 1개의 데이터 조회            
        )

        # 비동기 쿼리 실행
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        law_response = Law010_Response(
            msg_cd="00",  # 성공 코드
            msg="Success"
        )
        # 데이터가 limit + 1개로 조회되었다면 추가 데이터가 존재함 (exists_yn = "Y")
        if len(rows) > limit:
            law_response.exists_yn = "Y"
            rows = rows[:limit]  # limit 만큼만 데이터 자르기
        else:
            law_response.exists_yn = "N"

        if rows:
            law_response.conti_last_idx =  start_idx + len(rows) - 1

        # 조회된 데이터를 Ifi10Law_Response로 변환하여 output에 추가
        law_response.output = [Ifi10Law_Response(**row.__dict__) for row in rows]

        # count는 조회된 데이터의 개수로 설정 (limit 개수에 해당하는 값)
        law_response.count = len(law_response.output)

        return law_response   
    
    async def run_r011(self, req: Law011_Request) -> Law010_Response:
        ''' r011 변경 법큐정보 조회'''
        if req.all_yn == "Y":
            return await self.run_r011_all(req)
        else:
            return await self.run_r011_paging(req) 