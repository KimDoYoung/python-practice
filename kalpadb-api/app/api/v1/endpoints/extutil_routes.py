# extutil_routes.py
"""
모듈 설명: 
    -  외부 유틸리티 기능을 제공하는 API 엔드포인트를 정의합니다.
주요 기능:
    -  /hanja : 네이버 한자 사전에서 한자 리스트를 가져오는 기능
    -  /extract/words : 텍스트를 받아서 명사만 추출하는 기능
    -  /sol2lun/{ymd_list} : 양력->음력으로 변환하는 기능
    -  /kofic/movie/search : 영화진흥위원회(KOFIC)에서 영화 검색하는 기능
    -  /kofic/movie/detail/{movieCd} : 영화진흥위원회(KOFIC)에서 영화 상세정보 검색하는 기능
    -  /emoji/search/{keyword} : 이모지 사이트에서 이모지 검색하는 기능
    

작성자: 김도영
작성일: 2024-12-07
버전: 1.0
"""
import json
import os
from typing import Dict, List, Union
from korean_lunar_calendar import KoreanLunarCalendar
from pydantic import ValidationError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup
import requests as http_requests

from app.core.database import get_session
from app.core.util import extract_nouns
from app.domain.extutil.extutil_schema import SolarLunarResponse, TextRequest
from app.core.logger import get_logger
from app.domain.extutil.extutil_service import ExtUtilService
from app.domain.extutil.kofic.kofic_schema import KoficDetailResponse, KoficErrorResponse, KoficSearchResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.domain.extutil.scrap_service import ScrapService


logger = get_logger(__name__)

router = APIRouter()

def get_driver() -> webdriver.Chrome:
    """
    Selenium WebDriver 객체를 생성하여 반환합니다.
    """
    options = Options()
    options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


@router.get("/hanja", summary="Retrieve Hanja list using Selenium")
def get_hanja_list(query: str):
    """
    네이버 한자 사전에서 주어진 검색어로 한자 리스트를 가져옵니다.
    - **query**: 검색어 (예: 미혼)
    """
    url = f"https://hanja.dict.naver.com/#/search?query={query}"

    # WebDriver 가져오기
    driver = get_driver()
    try:
        # URL 로드
        driver.get(url)
        # 특정 요소가 로드될 때까지 기다림 (최대 10초)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchPage_entry"))
        )

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(page_source, "html.parser")
        div_result = soup.find("div", id="searchPage_entry")
        if not div_result:
            raise HTTPException(status_code=404, detail="Search results not found.")

        # div.row에서 한자 추출
        div_rows = div_result.find_all("div", class_="row")
        hanja_list = []
        for row in div_rows:
            origin_div = row.find("div", class_="origin")
            if origin_div:
                anchor = origin_div.find("a", class_="link", lang="zh")
                if anchor and anchor.text.strip():
                    hanja_list.append(anchor.text.strip())

        return {"query": query, "hanja_list": hanja_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        # WebDriver 종료
        driver.quit()


@router.post("/extract/words", summary="텍스트에서 단어 추출")
def extract_korean_words(request: TextRequest)->List[str]:
    ''' 텍스트를 받아서 그 중에서 명사만 추출하여 반환합니다. '''
    list = extract_nouns(request.text)
    list.sort()
    return list

def solYmd2lunYmd(solYmd):
    calendar = KoreanLunarCalendar()
    y = int(solYmd[:4])
    M = int(solYmd[4:6])
    d = int(solYmd[6:])

    calendar.setSolarDate(y, M, d)

    # Lunar Date (ISO Format)
    lunarDate = calendar.LunarIsoFormat().replace('-', '') # 20201208
    logger.debug(f"solYmd2lunYmd: {solYmd} -> {lunarDate}")
    return lunarDate

@router.get("/sol2lun/{ymd_list}", summary="양력->음력으로 변환", response_model=List[SolarLunarResponse])
def sol2lun(ymd_list: str, db: AsyncSession = Depends(get_session))->List[str]:
    ''' 양력 날짜를 음력으로 변환하여 반환합니다. ymd_list ymd|ymd... 형식 '''
    ymd_array = ymd_list.split('|')
    extutil_service = ExtUtilService(db)
    lunYmdArray = extutil_service.sol2lun_array(ymd_array)
    return lunYmdArray

@router.get("/kofic/movie/search", summary="영화진흥위원회(KOFIC)에서 제목으로영화리스트 찾기", response_model=Union[KoficSearchResponse, KoficErrorResponse])
def kofic_movie_search(query: str, year: str = '') -> KoficSearchResponse:
    ''' 영화진흥위원회(KOFIC)에서 주어진 검색어로 영화를 찾아 반환합니다. '''
    url = f"https://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
# &movieNm=%ED%86%A0%ED%83%88
# &curPage=1
# &itemPerPage=100 
# &prdtStartYear=2021   
    KOFIC_API_KEY = os.getenv("KOFIC_API_KEY")
    url += f"?key={KOFIC_API_KEY}"
    if year:
        url += f"&movieNm={query}&prdtStartYear={year}"
    else:
        url += f"&movieNm={query}"
    url += "&curPage=1&itemPerPage=100"
    try:
        # API 호출
        response = http_requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data, indent=4, ensure_ascii=False))
        # 정상 응답 처리
        try:
            result = KoficSearchResponse(**data)
            return result
        except ValidationError as e:
            # 오류 응답 처리
            error_response = KoficErrorResponse(**data)
            return error_response
    except http_requests.RequestException as e:
        # HTTP 요청 실패 시 FastAPI 예외로 변환
        raise HTTPException(status_code=500, detail=f"API 요청 실패: {e}")
    except ValidationError as e:
        # 데이터 파싱 실패 시 FastAPI 예외로 변환
        raise HTTPException(status_code=400, detail=f"데이터 파싱 오류: {e}")

@router.get("/kofic/movie/detail/{movieCd}", summary="영화진흥위원회(KOFIC)에서 영화 상세정보 찾기", response_model=Union[KoficDetailResponse, KoficErrorResponse])
def kofic_movie_detail(movieCd: str):
    ''' 영화진흥위원회(KOFIC)에서 주어진 영화코드로 영화 상세정보를 찾아 반환합니다. '''
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
    KOFIC_API_KEY = os.getenv("KOFIC_API_KEY")
    url += f"?key={KOFIC_API_KEY}"
    url += f"&movieCd={movieCd}"
    try:
        # API 호출
        response = http_requests.get(url)
        response.raise_for_status()
        data = response.json()
        # 데이터 예쁘게 출력
        logger.debug(json.dumps(data, indent=4, ensure_ascii=False))
        # 정상 응답 처리
        try:
            result = KoficDetailResponse(**data)
            return result
        except ValidationError as e:
            # 오류 응답 처리
            error_response = KoficErrorResponse(**data)
            return error_response
    except http_requests.RequestException as e:
        # HTTP 요청 실패 시 FastAPI 예외로 변환
        raise HTTPException(status_code=500, detail=f"API 요청 실패: {e}")
    except ValidationError as e:
        # 데이터 파싱 실패 시 FastAPI 예외로 변환
        raise HTTPException(status_code=400, detail=f"데이터 파싱 오류: {e}")


@router.get("/emoji/search/{keyword}", summary="이모지site에서 이모지 찾기", response_model=Dict[str, str])
def emoji_search(keyword: str):
    service = ScrapService()
    result = service.fetch_emojis_with_labels(keyword)
    logger.debug(result)
    return result