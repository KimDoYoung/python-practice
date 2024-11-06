
# class LawService:

#     @staticmethod
#     async def get_all_laws() -> List[Ifi10Law]:
#         """Ifi10Law 테이블에서 모든 법 정보를 가져옵니다."""
#         stmt = select(Ifi10Law).order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)
#         async with get_session() as session:
#             result = await session.execute(stmt)
#             return result.scalars().all()

#     @staticmethod
#     async def get_laws_with_pagination(start_idx: int, limit: int) -> List[Ifi10Law]:
#         """페이징을 적용하여 Ifi10Law 테이블에서 법 정보를 가져옵니다."""
#         stmt = (
#             select(Ifi10Law)
#             .order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)
#             .offset(start_idx)
#             .limit(limit + 1)
#         )
#         async with get_session() as session:
#             result = await session.execute(stmt)
#             return result.scalars().all()

#     @staticmethod
#     def build_law_response(rows, msg: str = "Success", start_idx: int = 0, limit: int = None) -> Law010_Response:
#         """Law010_Response 객체를 생성합니다."""
#         response = Law010_Response(msg_cd="00", msg=msg)
#         response.output = [Ifi10Law_Response(**row.__dict__) for row in rows]
#         response.count = len(response.output)

#         # 페이징 처리
#         if limit and len(rows) > limit:
#             response.exists_yn = "Y"
#             response.output = response.output[:limit]
#         else:
#             response.exists_yn = "N"

#         if rows:
#             response.conti_last_idx = start_idx + len(response.output) - 1

#         return response

#     @staticmethod
#     async def run_r010(req: Law010_Request) -> Law010_Response:
#         """법큐정보 조회"""
#         if req.all_yn == "Y":
#             rows = await LawService.get_all_laws()
#             return LawService.build_law_response(rows)
#         else:
#             rows = await LawService.get_laws_with_pagination(req.conti_start_idx, req.conti_limit)
#             return LawService.build_law_response(rows, start_idx=req.conti_start_idx, limit=req.conti_limit)

#     @staticmethod
#     async def field_mapping(layout_cd: str) -> dict:
#         """법큐 필드 매핑 정보 추출"""
#         stmt = (
#             select(func.substr(Ifi92ApiLayout.ifi92_element_nm, 2).label('ifi92_element_nm'), Ifi92ApiLayout.ifi92_link_column)
#             .where(
#                 Ifi92ApiLayout.ifi92_layout_cd == layout_cd,
#                 Ifi92ApiLayout.ifi92_message_cd == 'RES',
#                 Ifi92ApiLayout.ifi92_component_cd == 'B',
#                 Ifi92ApiLayout.ifi92_link_column.isnot(None)
#             )
#             .order_by(Ifi92ApiLayout.ifi92_seq)
#         )
#         async with get_session() as session:
#             result = await session.execute(stmt)
#             rows = result.fetchall()
#         return {row.ifi92_element_nm: row.ifi92_link_column for row in rows}

#     @staticmethod
#     async def get_changed_laws(start_ymd: str, end_ymd: str, start_idx: int = None, limit: int = None) -> list:
#         """변경된 법큐 정보 조회 r011"""
#         subquery = (
#             select(Ifi11LawRecord.ifi11_class_tree_cd, Ifi11LawRecord.ifi11_deadline_id)
#             .where(
#                 Ifi11LawRecord.ifi11_dml_type.notin_(['DELETE']),
#                 Ifi11LawRecord.ifi11_dml_date.between(func.to_date(start_ymd, 'YYYYMMDD'), func.to_date(end_ymd, 'YYYYMMDD'))
#             )
#             .subquery()
#         )
#         stmt = (
#             select(Ifi10Law)
#             .where(
#                 tuple_(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id).in_(subquery)
#             )
#             .order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)
#         )
#         if start_idx is not None and limit is not None:
#             stmt = stmt.offset(start_idx).limit(limit + 1)

#         async with get_session() as session:
#             result = await session.execute(stmt)
#             return result.scalars().all()

#     @staticmethod
#     async def run_r011(req: Law011_Request) -> Law010_Response:
#         """r011 변경 법큐정보 조회"""
#         rows = await LawService.get_changed_laws(
#             start_ymd=req.modi_start_date,
#             end_ymd=req.modi_end_date,
#             start_idx=req.conti_start_idx if req.all_yn != "Y" else None,
#             limit=req.conti_limit if req.all_yn != "Y" else None
#         )
#         return LawService.build_law_response(rows, start_idx=req.conti_start_idx, limit=req.conti_limit if req.all_yn != "Y" else None)
#-----------------------------------------------------------

from sqlalchemy import func, select, tuple_

from backend.app.domain.ifi.ifi10.ifi10_law_model import Ifi10Law
from backend.app.domain.ifi.ifi10.ifi10_law_schema import Ifi10Law_Response
from backend.app.domain.ifi.ifi11.ifi11_law_record_model import Ifi11LawRecord
from backend.app.domain.ifi.ifi92.ifi92_api_layout_model import Ifi92ApiLayout
from backend.app.domain.service.law.law_schema import Law010_Request, Law010_Response, Law011_Request
from backend.app.core.database import get_session
        
class LawService:

    @staticmethod
    async def run_r010_all(req: Law010_Request) -> Law010_Response:
        ''' r010 법큐정보 조회 (전체) '''
        stmt = (
            select(Ifi10Law)
            .order_by(Ifi10Law.ifi10_law_cd, Ifi10Law.ifi10_deadline_id)  # 정렬 조건
        )

        # 비동기 쿼리 실행
        async with get_session() as session:
            result = await session.execute(stmt)
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
    
    @staticmethod
    async def run_r010_paging(req: Law010_Request) -> Law010_Response:
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
        async with get_session() as session:
            result = await session.execute(stmt)
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

    @staticmethod
    async def run_r010( req: Law010_Request) -> Law010_Response:
        ''' r010 법큐정보 조회'''
        if req.all_yn == "Y":
            return await LawService.run_r010_all(req)
        else:
            return await LawService.run_r010_paging(req) 

    @staticmethod
    async def field_mapping( layout_cd: str):
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
        async with get_session() as session:
            result = await session.execute(stmt)
            rows = result.fetchall()

        # field_mapping 생성
        field_mapping = {row.ifi92_element_nm: row.ifi92_link_column for row in rows}

        return field_mapping

    @staticmethod
    async def run_r011_all( req: Law011_Request) -> Law010_Response:
        start_ymd = req.modi_start_date
        end_ymd = req.modi_end_date
        subquery = (
            select(Ifi11LawRecord.ifi11_class_tree_cd, Ifi11LawRecord.ifi11_deadline_id)
            .where(
                Ifi11LawRecord.ifi11_dml_type.notin_(['DELETE']),
                Ifi11LawRecord.ifi11_dml_date.between(func.to_date(start_ymd, 'YYYYMMDD'), func.to_date(end_ymd, 'YYYYMMDD'))
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
        async with get_session() as session:
            result = await session.execute(stmt)
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

    @staticmethod
    async def run_r011_paging(req: Law011_Request) -> Law010_Response:
        start_idx = req.conti_start_idx
        limit = req.conti_limit
        start_ymd = req.modi_start_date
        end_ymd = req.modi_end_date
        subquery = (
            select(Ifi11LawRecord.ifi11_class_tree_cd, Ifi11LawRecord.ifi11_deadline_id)
            .where(
                Ifi11LawRecord.ifi11_dml_type.notin_(['DELETE']),
                Ifi11LawRecord.ifi11_dml_date.between(func.to_date(start_ymd, 'YYYYMMDD'), func.to_date(end_ymd, 'YYYYMMDD'))
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
        async with get_session() as session:
            result = await session.execute(stmt)
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

    @staticmethod
    async def run_r011(req: Law011_Request) -> Law010_Response:
        ''' r011 변경 법큐정보 조회'''
        if req.all_yn == "Y":
            return await LawService.run_r011_all(req)
        else:
            return await LawService.run_r011_paging(req) 