
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup

from app.core.util import extract_nouns
from app.domain.extutil.extutil_schema import TextRequest

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
        driver.implicitly_wait(3)  # 동적 로딩 대기

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
