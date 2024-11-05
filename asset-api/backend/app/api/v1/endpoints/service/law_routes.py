from datetime import datetime
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.logger import get_logger
from backend.app.core.database import get_session
from backend.app.domain.service.law.law_schema import Law010_Request, Law011_Request
from backend.app.domain.service.law.law_service import LawService

logger = get_logger()
router = APIRouter()

async def build_modified_output(output: List[Dict], field_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
    """필드 매핑에 따라 응답 데이터를 가공합니다."""
    modified_output = []
    for idx, item in enumerate(output):
        ordered_item = {
            'base_dt': datetime.now().strftime("%Y%m%d"),
            'seq': idx + 1
        }
        # 필드 매핑에 따라 새로운 키로 데이터를 변환
        for new_key, original_key in field_mapping.items():
            if original_key in item:
                ordered_item[new_key] = item[original_key]
        modified_output.append(ordered_item)
    return modified_output

async def build_response_data(resp, field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """응답 데이터를 최종 형식으로 가공하고 로깅합니다."""
    resp_dict = resp.model_dump()
    modified_output = await build_modified_output(resp_dict['output'], field_mapping)
    response_data = {
        "msg_cd": resp_dict['msg_cd'],
        "msg": resp_dict['msg'],
        "count": resp_dict['count'],
        "exists_yn": resp_dict['exists_yn'],
        "conti_last_idx": resp_dict['conti_last_idx'],
        "output": modified_output
    }

    # 디버그 로깅
    logger.debug("======================================")
    logger.debug(f"Modified resp: {response_data}")
    logger.debug("======================================")
    return response_data

@router.get("/r010", response_model=dict[str, Any], tags=["법규정보"])
async def r010(
    conti_limit: int = Query(10, ge=1, le=1000, description="연속 조회 LIMIT"),
    conti_start_idx: int = Query(0, ge=0, description="연속 조회 START INDEX"),
    all_yn: str = Query("N", description="연속 조회 여부 (Y/N)"),
    db: AsyncSession = Depends(get_session)
):
    """법규정보 서비스"""
    field_mapping = await LawService.field_mapping('LAW010')
    req = Law010_Request(conti_limit=conti_limit, conti_start_idx=conti_start_idx, all_yn=all_yn)
    resp = await LawService.run_r010(req)
    return await build_response_data(resp, field_mapping)

@router.get("/r011", response_model=dict[str, Any], tags=["변경법규정보"])
async def r011(
    all_yn: str = Query("N", description="전체 조회 여부"),
    modi_start_date: str = Query("", description="변경법규 조회시작일"),
    modi_end_date: str = Query("", description="변경법규 조회종료일"),
    conti_limit: int = Query(10, ge=1, le=1000, description="연속 조회 LIMIT"),
    conti_start_idx: int = Query(0, ge=0, description="연속 조회 START INDEX"),
    db: AsyncSession = Depends(get_session)
):
    """변경 법규정보 서비스"""
    field_mapping = await LawService.field_mapping('LAW011')
    req = Law011_Request(
        conti_limit=conti_limit,
        conti_start_idx=conti_start_idx,
        all_yn=all_yn,
        modi_start_date=modi_start_date,
        modi_end_date=modi_end_date
    )
    resp = await LawService.run_r011(req)
    return await build_response_data(resp, field_mapping)

# from datetime import datetime
# from typing import Any
# from fastapi import APIRouter, Depends, Query
# from sqlalchemy.ext.asyncio import AsyncSession
# from backend.app.core.logger import get_logger
# from backend.app.core.database import get_session
# from backend.app.domain.service.law.law_schema import Law010_Request, Law011_Request
# from backend.app.domain.service.law.law_service import LawService
# logger = get_logger()

# router = APIRouter()

# @router.get("/r010",  response_model=dict[str, Any], tags=["법규정보"])
# async def r010(
#     conti_limit: int = Query(10, ge=1, le=1000, description="연속 조회 LIMIT"),
#     conti_start_idx: int = Query(0, ge=0, description="연속 조회 START INDEX"),
#     all_yn: str = Query("N", description="연속 조회 여부 (Y/N)"),
#     db: AsyncSession = Depends(get_session)
# ):
#     '''법규정보 서비스 '''
#     # 포함시켜야할 필드들 추출 
#     field_mapping = await LawService.field_mapping('LAW010')
#     # law10에서 데이터 추출
#     req = Law010_Request(conti_limit=conti_limit, conti_start_idx=conti_start_idx, all_yn=all_yn)
#     resp = await LawService.run_r010(req)
#     resp_dict = resp.model_dump()

#     # output 가공
#     modified_output = []

#     for idx, item in enumerate(resp_dict['output']):
#         # 새로운 딕셔너리로 순서 보장
#         ordered_item = {
#             'base_dt': datetime.now().strftime("%Y%m%d"),  # base_dt 먼저 추가
#             'seq': idx + 1  # seq 추가
#         }

#         # 필드 매핑에 따라 새로운 키로 데이터를 변환
#         for new_key, original_key in field_mapping.items():
#             # 만약 매핑된 필드가 item에 있으면 새로운 키로 매핑
#             if original_key in item:
#                 ordered_item[new_key] = item[original_key]

#         modified_output.append(ordered_item)

#     # 최종적으로 가공된 데이터를 반환
#     response_data = {
#         "msg_cd": resp_dict['msg_cd'],
#         "msg": resp_dict['msg'],
#         "count": resp_dict['count'],
#         "exists_yn": resp_dict['exists_yn'],
#         "conti_last_idx": resp_dict['conti_last_idx'],
#         "output": modified_output
#     }

#     logger.debug("======================================")
#     logger.debug(f"Modified resp: {response_data}")
#     logger.debug("======================================")

#     return response_data    


# @router.get("/r011",  response_model=dict[str, Any], tags=["변경법규정보"])
# async def r011(
#     all_yn: str = Query("N", description="전체 조회 여부"),
#     modi_start_date: str = Query("", description="변경법규 조회시작일"),
#     modi_end_date: str = Query("", description="변경법규 조회종료일"),
#     conti_limit: int = Query(10, ge=1, le=1000, description="연속 조회 LIMIT"),
#     conti_start_idx: int = Query(0, ge=0, description="연속 조회 START INDEX"),
#     db: AsyncSession = Depends(get_session)
# ):
#     # service = LawService(db)
#     # 포함시켜야할 필드들 추출 
#     field_mapping = await LawService.field_mapping('LAW011')
#     # law10에서 데이터 추출
#     req = Law011_Request(conti_limit=conti_limit, conti_start_idx=conti_start_idx, all_yn=all_yn, modi_start_date=modi_start_date, modi_end_date=modi_end_date)
#     resp = await LawService.run_r011(req)
#     resp_dict = resp.model_dump()
    
#     # 가져온 dict를 
#     modified_output = []

#     for idx, item in enumerate(resp_dict['output']):
#         # 새로운 딕셔너리로 순서 보장
#         ordered_item = {
#             'base_dt': datetime.now().strftime("%Y%m%d"),  # base_dt 먼저 추가
#             'seq': idx + 1  # seq 추가
#         }

#         # 필드 매핑에 따라 새로운 키로 데이터를 변환
#         for new_key, original_key in field_mapping.items():
#             # 만약 매핑된 필드가 item에 있으면 새로운 키로 매핑
#             if original_key in item:
#                 ordered_item[new_key] = item[original_key]

#         modified_output.append(ordered_item)

#     # 최종적으로 가공된 데이터를 반환
#     response_data = {
#         "msg_cd": resp_dict['msg_cd'],
#         "msg": resp_dict['msg'],
#         "count": resp_dict['count'],
#         "exists_yn": resp_dict['exists_yn'],
#         "conti_last_idx": resp_dict['conti_last_idx'],
#         "output": modified_output
#     }

#     logger.debug("======================================")
#     logger.debug(f"Modified resp: {response_data}")
#     logger.debug("======================================") 
    
#     return response_data    