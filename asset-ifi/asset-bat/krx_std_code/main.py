import asyncio
from datetime import datetime, timezone
import json
from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import func, select
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
from common.database import Database
from common.domain.model.ifi20_dart_corp_model import IFI20DartCorp
from common.domain.schema.jibun_stock_schema import JibunStockResponse
from common.utils import generate_korean_pronunciation_variants
import math
from common.settings import config
import os

# Globa변수 
database = Database()
main_window = None
DEBUG = config.DEBUG
data_folder = config.DATA_FOLDER
# 데이터 폴더 생성
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    
# 웹 드라이버 설정
def setup_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


async def fetch_latest_ifi21_data() -> List[str]:
    ''' ifi21에서 최신 날짜의 데이터를 조회하여 대상 회사명 리스트를 반환하는 함수 '''
    corp_name_list = []
    market_type = {
        'Y': '유가',
        'K': '코스닥',
        'N': '코넥스',
        'E': '기타'
    }
    try:
        rows = await database.fetch("""
            SELECT ifi21_response FROM ifi21_api_data
            WHERE ifi21_date = (
                SELECT max(ifi21_date) FROM ifi21_api_data
            ) AND ifi21_status_cd = '000'
        """)

        for json_data in rows:
            try:
                # JSON 데이터를 JibunStockResponse 모델로 변환
                response_data = JibunStockResponse.model_validate_json(json_data)

                # 각 그룹과 그룹 내 항목에서 corp_name 추출
                found = False
                for group in response_data.group or []:
                    for item in group.list:
                        if item.corp_name:
                            name = item.corp_name + '|' + item.corp_code + '|' + market_type[item.corp_cls]
                            if name not in corp_name_list:
                                corp_name_list.append(name)
                                found = True
                                break
                    if found:
                        break            

            except json.JSONDecodeError as e:
                print(f"JSON 파싱 오류: {e}")
            except ValidationError as e:
                print(f"데이터 검증 오류: {e}")

    except Exception as e:
        print(f"데이터베이스 오류: {e}")

    return corp_name_list



async def process_search_results(driver, corp_name, corp_cd, corp_cls):
    '''맨 마지막 페이지로 이동해서 역순으로 클릭해 가면서 찾는다.'''
    global main_window

    def get_text_or_none(driver, xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return None

    found = False

    # 전체 결과 수(`total_count`)를 통해 `total_pages` 계산
    try:
        total_count = int(driver.find_element(By.ID, "totPage").text)  # 실제로는 전체 결과 수
        total_pages = math.ceil(total_count / 15)  # 한 페이지당 15개 표시
    except Exception as e:
        print(f"전체 결과 수를 확인할 수 없습니다: {e}")
        return  # 오류 발생 시 함수 종료

    # 검색 결과가 없는 경우 종료
    if total_count == 0:
        print("********************************************************")
        print(f"검색 결과가 없습니다 (회사명: {corp_name})")
        print("********************************************************")
        return

    # 맨 마지막 페이지부터 시작해 역순으로 순회
    page_index = total_pages
    while page_index >= 1:
        # 총 페이지가 1개 이상일 때만 페이지 이동
        if total_pages > 1:
            driver.execute_script(
                "document.JLDINF05200.pageIndex.value = arguments[0]; fn_goPage();", page_index
            )
            # 다음 페이지 로드 완료 대기 (예: 페이지 번호를 나타내는 요소가 로드될 때까지 대기)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".type-00.list tbody tr"))
            )

        # 현재 페이지의 검색 결과 `tr` 태그 순회 (역순으로)
        result_rows = driver.find_elements(By.CSS_SELECTOR, ".type-00.list tbody tr")
        
        for row in reversed(result_rows):  # `reversed()`로 `tr` 요소를 역순으로 순회
            try:
                # 각 행의 첫 번째 셀에서 발행기관 코드 링크 클릭
                link_element = row.find_element(By.CSS_SELECTOR, "td.first a")
                link_element.click()  # 팝업창 열기

                # 새 창이 열릴 때까지 대기 (기존 창보다 handles가 1개 더 많아질 때까지)
                WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
                # 팝업창에서 데이터 추출
                driver.switch_to.window(driver.window_handles[-1])  # 새 창으로 전환

                # 팝업 창의 로딩이 완료될 때까지 대기
                # WebDriverWait(driver, 10).until(
                #     lambda d: d.execute_script("return document.readyState") == "complete"
                # )
                # try:
                #     WebDriverWait(driver, 10).until(
                #         EC.presence_of_element_located((By.TAG_NAME, "body"))
                #     )
                # except Exception as e:
                await asyncio.sleep(5)  # 대기 시간 추가

                # 페이지 소스를 저장
                if DEBUG:
                    with open(f"{data_folder}/popup_page_source_{corp_name}_{page_index}.html", "w", encoding="utf-8") as file:
                        file.write(driver.page_source)                             
                
                # 각 요소를 get_text_or_none 함수로 추출
                iss_corp_code = get_text_or_none(driver, "//th[text()='발행기관코드']/following-sibling::td")
                iss_corp_nm = get_text_or_none(driver, "//th[text()='발행기관명(한글)']/following-sibling::td/a")
                iss_corp_snm = get_text_or_none(driver, "//th[text()='발행기관명(한글약명)']/following-sibling::td")
                iss_corp_enm = get_text_or_none(driver, "//th[text()='발행기관명(영문)']/following-sibling::td")
                corp_reg_no = get_text_or_none(driver, "//th[text()='법인등록번호']/following-sibling::td")
                biz_reg_no = get_text_or_none(driver, "//th[text()='사업자등록번호']/following-sibling::td")
                addr = get_text_or_none(driver, "//th[text()='주소']/following-sibling::td[@colspan='3']")
                eaddr = get_text_or_none(driver, "//th[text()='영문주소']/following-sibling::td[@colspan='3']")
                ceo = get_text_or_none(driver, "//th[text()='대표이사']/following-sibling::td")
                tel = get_text_or_none(driver, "//th[text()='대표전화']/following-sibling::td")
                homepage = get_text_or_none(driver, "//th[text()='홈페이지']/following-sibling::td/a")
                market_type = get_text_or_none(driver, "//th[text()='시장구분']/following-sibling::td")
                list_yn = get_text_or_none(driver, "//th[text()='상장여부']/following-sibling::td")
                industry_class = get_text_or_none(driver, "//th[text()='업태']/following-sibling::td")
                industry_item = get_text_or_none(driver, "//th[text()='업종']/following-sibling::td")
                
                print(f"팝업 페이지 해석 페이지: {page_index} 회사명: {corp_name},  : 회사명 {iss_corp_nm}  약어: {iss_corp_snm}, 시장구분: {market_type}") 
                # 추출한 데이터를 딕셔너리로 구성
                corp_data = {
                    "ifi20_iss_corp_cd": iss_corp_code,
                    "ifi20_iss_corp_nm": iss_corp_nm,
                    "ifi20_iss_corp_snm": iss_corp_snm,
                    "ifi20_iss_corp_enm": iss_corp_enm,
                    "ifi20_corp_reg_no": corp_reg_no.replace("-", "").strip() if corp_reg_no else None,
                    "ifi20_biz_reg_no": biz_reg_no.replace("-", "").strip() if biz_reg_no else None,
                    "ifi20_addr": addr,
                    "ifi20_eaddr": eaddr,
                    "ifi20_ceo": ceo,
                    "ifi20_tel": tel,
                    "ifi20_homepage": homepage,
                    "ifi20_market_type": market_type,
                    "ifi20_list_yn": list_yn,
                    "ifi20_industry_class": industry_class,
                    "ifi20_industry_item": industry_item
                }

                # 회사 약어명과 일치하는지 체크 일치하면 찾는 것이라고 판단한다. 
                check = False
                if total_count == 1: 
                    if corp_cls in corp_data["ifi20_market_type"]:
                        check = True
                else:
                    if corp_data["ifi20_iss_corp_snm"] == corp_name and corp_cls in corp_data["ifi20_market_type"]:
                        check = True
                    
                if check:
                    found = True
                    await save_to_ifi20(corp_name, corp_cd, corp_data)  # 추출한 데이터 저장
                    if main_window != driver.current_window_handle: # 팝업창이 열려있으면 닫기
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])                    
                    break  # 찾으면 루프 종료

                if main_window != driver.current_window_handle: # 팝업창이 열려있으면 닫기
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"데이터 추출 오류 (회사명: {corp_name}, 페이지: {page_index}): {e}")
                if main_window != driver.current_window_handle: # 팝업창이 열려있으면 닫기
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])   

            # 목표 데이터가 발견되면 함수 종료
            if found:
                break

        # 이전 페이지로 이동
        page_index -= 1
# 스크래핑 수행 함수
async def perform_scraping(corp_names: List[str]):
    global main_window
    
    driver = setup_webdriver()
    driver.get("https://isin.krx.co.kr/corp/corpList.do?method=corpInfoList")
    
    main_window = driver.current_window_handle
    
    for corp_name_and_cd in corp_names:
        corp_name, corp_cd, corp_cls = corp_name_and_cd.split('|')
        search_variants = generate_korean_pronunciation_variants(corp_name)
        
        for search_name in search_variants:
            try:
                # 검색어 입력
                search_box = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "searchWord"))
                )
                search_box.clear()
                search_box.send_keys(search_name)
                search_box.send_keys(Keys.RETURN)
                
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # 검색 결과 확인
                tot_page_element = driver.find_element(By.ID, "totPage")
                total_count = int(tot_page_element.text)

                if total_count == 0:
                    print(f"검색 결과가 없습니다: {corp_name}-{corp_cd} ({search_name})")
                    continue  # 검색 결과가 없으면 다음 검색어로 이동

                # 검색 결과 처리 함수 호출 (페이지 단위로 처리)
                await process_search_results(driver, corp_name, corp_cd, corp_cls)

            except Exception as e:
                print(f"오류 발생 (회사명: {corp_name}, DART코드 {corp_cd} 검색어: {search_name}): {e}")

    driver.quit()

# 스크래핑 데이터 DB 저장

async def save_to_ifi20(corp_name:str, corp_cd: str, data: dict):
    '''결과 데이터를 ifi20_dart_corp 테이블에 update한다'''
    async with database.get_connection() as session:
        
        # ifi20_dart_corp_cd 필드를 기준으로 레코드 조회
        result = await session.execute(select(IFI20DartCorp).where(IFI20DartCorp.ifi20_dart_corp_cd == corp_cd))
        existing_record = result.scalars().first()

        if existing_record:
            # 업데이트할 필드 목록
            update_fields = [
                "ifi20_iss_corp_cd", "ifi20_iss_corp_nm", "ifi20_iss_corp_snm", "ifi20_iss_corp_enm",
                "ifi20_corp_reg_no", "ifi20_biz_reg_no", "ifi20_addr", "ifi20_eaddr",
                "ifi20_ceo", "ifi20_tel", "ifi20_homepage", "ifi20_market_type", 
                "ifi20_list_yn", "ifi20_industry_class", "ifi20_industry_item"
            ]
            # 필드 값 설정
            for field in update_fields:
                if field in data:
                    setattr(existing_record, field, data[field])

            # 작업일시 필드 업데이트
            existing_record.ifi20_work_date = func.now()
            
            print(f"기존 레코드 업데이트 완료: {corp_name} : DART코드 {corp_cd}")

            # 데이터베이스 커밋 및 오류 처리
            try:
                await session.commit()
                print(f"KRX발행기관정보로 ifi20 데이터 UPDATE  성공: {data}")
            except Exception as e:
                await session.rollback()
                print(f"KRX발행기관정보로 ifi20 데이터 UPDATE 오류: {e}")
        else: # 존재하지 않으면 무시한다. 즉 ifi20에 corp_code가 없으면 무시한다.
            print(f"ifi20에 {corp_name} DART코드:{corp_cd} 가 존재하지 않습니다. 추가합니다")
            result = await session.execute(select(func.f_create_batchseq()))
            ifi20_dart_corp_id = result.scalar()  # 함수에서 반환된 ID 값            
            # ifi20 테이블에 레코드 추가
            new_record = IFI20DartCorp(
                ifi20_dart_corp_id= ifi20_dart_corp_id,
                ifi20_dart_corp_cd=corp_cd,
                ifi20_dart_corp_nm=corp_name,
                ifi20_iss_corp_cd=data["ifi20_iss_corp_cd"],
                ifi20_iss_corp_nm=data["ifi20_iss_corp_nm"],
                ifi20_iss_corp_snm=data["ifi20_iss_corp_snm"],
                ifi20_iss_corp_enm=data["ifi20_iss_corp_enm"],
                ifi20_corp_reg_no=data["ifi20_corp_reg_no"],
                ifi20_biz_reg_no=data["ifi20_biz_reg_no"],
                ifi20_addr=data["ifi20_addr"],
                ifi20_eaddr=data["ifi20_eaddr"],
                ifi20_ceo=data["ifi20_ceo"],
                ifi20_tel=data["ifi20_tel"],
                ifi20_homepage=data["ifi20_homepage"],
                ifi20_market_type=data["ifi20_market_type"],
                ifi20_list_yn=data["ifi20_list_yn"],
                ifi20_industry_class=data["ifi20_industry_class"],
                ifi20_industry_item=data["ifi20_industry_item"],
                ifi20_work_date=datetime.now(timezone.utc)
            )
            session.add(new_record)
            # 데이터베이스 커밋 및 오류 처리
            try:
                await session.commit()
                print(f"ifi20에 데이터없음 KRX발행기관에서 ifi20 데이터 INSERT 성공: {data}")
            except Exception as e:
                await session.rollback()
                print(f"ifi20에 데이터없음 KRX발행기관에서 ifi20 데이터 INSERT 오류: {e}")

# 메인 실행 함수
async def main():
    # 대상조회
    corp_names = await fetch_latest_ifi21_data()
    
    if DEBUG:
        # corp_names를 파일에 저장
        with open(f"{data_folder}/corp_names.dat", "w", encoding="utf-8") as file:
            for corp_name in corp_names:
                file.write(corp_name + "\n")        
    # corp_names=["키움제10호기업인수목적|01877126|기타"]
    await perform_scraping(corp_names)

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("KRX에서 발행기관조회 ifi20채우기 시작: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("--------------------------------------------------")
    asyncio.run(main())
    print("--------------------------------------------------")
    print("KRX에서 발행기관조회 ifi20채우기 종료: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("--------------------------------------------------")
