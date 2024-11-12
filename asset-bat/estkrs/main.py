import asyncio
from datetime import datetime, timedelta

from pydantic import ValidationError
from sqlalchemy import func, select, text
from common.database import Database
from common.domain.ifi21_api_data_model import Ifi21ApiData
from gosi_list_schema import GosiListParam, GosiListResponse
from jibun_stock_schema import JibunStockParam, JibunStockResponse
from common.settings import config
from urllib.parse import urlencode
import aiohttp

# Constants
URL_GOSI_LIST = "https://opendart.fss.or.kr/api/list.json"
URL_JIBUN_STOCK = "https://opendart.fss.or.kr/api/estkRs.json"
DATABASE_URL = config.DB_URL
DART_API_KEY = config.DART_API_KEY

# 날짜 설정 (오늘과 3개월 전)
TODAY = datetime.today().strftime('%Y%m%d')
THREE_MONTHS_AGO = (datetime.today() - timedelta(days=90)).strftime('%Y%m%d')


async def fetch_json(http_session, url, params):
    params = {k: v for k, v in params.items() if v is not None}
    
    full_url = f"{url}?{urlencode(params)}"
    print(f"지분증권 Request URL: {full_url}")  # 전체 URL 출력    
    
    async with http_session.get(url, params=params) as response:
        response.raise_for_status()  # Raise exception for HTTP errors
        return await response.json()


async def get_ifi91_config_api_id(db_session):
    ''' ifi91에서 config_api_id를 가져오는 함수 '''
    sql_query = text("""
        SELECT ifi91_config_api_id 
        FROM ifi91_config_api ica 
        WHERE ifi91_api_tr_cd = 'DART002' 
        LIMIT 1
    """)
    result = await db_session.execute(sql_query)
    return result.scalar()


async def main():
    database = Database()  # Database instance

    async with aiohttp.ClientSession() as http_session, database.get_connection() as db_session:
        # Step 1: GosiList 요청 (페이지 1, 100개씩, 3개월 범위) -> 모든 고유번호 데이터 가져오기
        params = GosiListParam(
            crtfc_key=DART_API_KEY,
            pblntf_detail_ty="C001",  # 증권신고(지분증권)
            bgn_de=THREE_MONTHS_AGO,
            end_de=TODAY,
            sort="date",
            sort_mth="desc",
            page_no=1,
            page_count=100,
        )

        page_no = 1
        all_items = []

        # 공시리스트의 모든 데이터를 가져와서 corp_code를 중복없이 가져온다.
        while True:
            params.page_no = page_no
            gosi_data = await fetch_json(http_session, URL_GOSI_LIST, params.model_dump())
            gosi_response = GosiListResponse(**gosi_data)
            all_items.extend(gosi_response.list)

            # 다음 페이지가 있는지 확인
            if page_no * params.page_count >= gosi_response.total_count:
                break
            page_no += 1
            # 안전장치
            if page_no > 10:
                break

        # Step 3: 중복되지 않은 corp_code 집합 생성
        corp_codes = {item.corp_code for item in all_items}

        # 먼저 91에서 api_id를 가져온다.
        ifi91_config_api_id = await get_ifi91_config_api_id(db_session)
        print(f"--> ifi91_config_api_id: {ifi91_config_api_id}")
        # Step 4-6: 각 corp_code에 대해 JibunStockParam 요청 및 데이터베이스 저장
        print(f"--> 구한 crop_code 갯수: {len(corp_codes)}")
        for corp_code in corp_codes:
            # JibunStockParam 생성
            jibun_params = JibunStockParam(
                crtfc_key=DART_API_KEY,
                corp_code=corp_code,
                bgn_de=THREE_MONTHS_AGO,
                end_de=TODAY
            )
            # f_create_batchseq() 함수를 호출하여 ifi21_api_data_id 생성
            result = await db_session.execute(select(func.f_create_batchseq()))
            ifi21_api_data_id = result.scalar()  # 함수에서 반환된 ID 값
            print(f"--> 채번 ifi91_config_api_id: {ifi91_config_api_id}")
            # JibunStockResponse 데이터 가져오기
            try:
                                
                jibun_data = await fetch_json(http_session, URL_JIBUN_STOCK, jibun_params.model_dump())
                jibun_response = JibunStockResponse(**jibun_data)
                success_yn = "true"
                company_nm = ""
                if jibun_response.status != "000":
                    success_yn = "false"
                else:
                    company_nm = jibun_response.group[0].list[0].corp_name
                # 데이터베이스에 insert
                new_record = Ifi21ApiData(
                    ifi21_api_data_id=ifi21_api_data_id,
                    ifi21_config_api_id=ifi91_config_api_id,
                    ifi21_date=datetime.now().date(),
                    ifi21_request=jibun_params.model_dump_json(),
                    ifi21_success_yn=success_yn,
                    ifi21_status_cd=jibun_response.status,
                    ifi21_status_msg=jibun_response.message,
                    ifi21_response=jibun_response.model_dump_json(),
                    ifi21_search1=corp_code,
                    ifi21_search2=company_nm
                )
                db_session.add(new_record)
                await db_session.commit()
                print(f"--> 성공 저장 ifi91_config_api_id: {ifi91_config_api_id}, corp_code: {corp_code}")
            # HTTP 요청 오류 처리
            except aiohttp.ClientResponseError as e:
                error_message = f"HTTP Error {e.status}: {e.message}"
                print(f"--> HTTP 오류: {error_message}")
                break
            except ValidationError as e:
                error_message = "Validation Error: " + str(e)
                print(f"--> 데이터 검증 오류: {error_message}")
                break                                
            except Exception as e:
                # 실패 시 로그 및 DB에 실패 기록 저장
                new_record = Ifi21ApiData(
                    ifi21_api_data_id=ifi21_api_data_id,
                    ifi21_config_api_id=ifi91_config_api_id,
                    ifi21_date=datetime.now().date(),
                    ifi21_request=jibun_params.model_dump_json(),
                    ifi21_success_yn="false",
                    ifi21_status_cd="-1",
                    ifi21_status_msg=str(e),
                    ifi21_response="",
                    ifi21_search1=corp_code,
                    ifi21_search2=None
                )
                db_session.add(new_record)
                await db_session.commit()
                print(f"--> 실패 저장 ifi91_config_api_id: {ifi91_config_api_id}, corp_code: {corp_code}")

# Bash에서 호출을 위한 진입점
if __name__ == "__main__":
    print("------------------------------------------------------")
    print("IF21 API 데이터 수집을 시작합니다.")
    print("------------------------------------------------------")
    asyncio.run(main())
    print("------------------------------------------------------")
    print("IF21 API 데이터 수집이 종료되었습니다")
    print("------------------------------------------------------")
    
