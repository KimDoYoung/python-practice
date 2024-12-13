# extutil_routes.py
"""
모듈 설명: 
    -  외부 유틸리티 기능을 제공하는 API 엔드포인트를 정의합니다.
주요 기능:
    -  /hanja : 네이버 한자 사전에서 한자 리스트를 가져오는 기능
    -  /extract/words : 텍스트를 받아서 명사만 추출하는 기능
    -  /sol2lun/{ymd_list} : 양력->음력으로 변환하는 기능

작성자: 김도영
작성일: 2024-12-07
버전: 1.0
"""
from typing import List
from korean_lunar_calendar import KoreanLunarCalendar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup

from app.core.util import extract_nouns
from app.domain.extutil.extutil_schema import SolarLunarResponse, TextRequest
from app.core.logger import get_logger

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
def sol2lun(ymd_list: str)->List[str]:
    ''' 양력 날짜를 음력으로 변환하여 반환합니다. ymd_list ymd|ymd... 형식 '''
    ymd_array = ymd_list.split('|')
    lunYmdArray = []
    for solYmd in ymd_array:
        lunYmd = solYmd2lunYmd(solYmd)
        sol_lun_response = SolarLunarResponse(solYmd=solYmd, lunYmd=lunYmd)
        lunYmdArray.append(sol_lun_response)
    return lunYmdArray