import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 전역 변수로 드라이버 선언
driver = None

def get_driver():
    """
    Selenium WebDriver를 초기화하거나 이미 초기화된 드라이버를 반환
    """
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저 창 숨기기
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")  # GPU 렌더링 비활성화
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def getGoSiList(frDate, toDate, pageIndex):
    # 요청 URL 및 헤더 설정
    url = "https://kind.krx.co.kr/disclosure/details.do"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    # POST 데이터
    data = {
    "method": "searchDetailsSub",
    "currentPageSize": 10,
    "pageIndex": 1,
    "orderMode": 1,
    "orderStat": "D",
    "forward": "details_sub",
    "disclosureType01": "",
    "disclosureType02": "",
    "disclosureType03": "",
    "disclosureType04": "",
    "disclosureType05": "",
    "disclosureType06": "",
    "disclosureType07": "",
    "disclosureType08": "",
    "disclosureType09": "",
    "disclosureType10": "",
    "disclosureType11": "",
    "disclosureType13": "",
    "disclosureType14": "",
    "disclosureType20": "",
    "pDisclosureType01": "",
    "pDisclosureType02": "",
    "pDisclosureType03": "",
    "pDisclosureType04": "",
    "pDisclosureType05": "",
    "pDisclosureType06": "",
    "pDisclosureType07": "",
    "pDisclosureType08": "",
    "pDisclosureType09": "",
    "pDisclosureType10": "",
    "pDisclosureType11": "",
    "pDisclosureType13": "",
    "pDisclosureType14": "",
    "pDisclosureType20": "",
    "searchCodeType": "",
    "repIsuSrtCd": "",
    "allRepIsuSrtCd": "",
    "oldSearchCorpName": "",
    "disclosureType": "",
    "disTypevalue": "",
    "reportNm": "",
    "reportCd": "",
    "searchCorpName": "",
    "business": "",
    "marketType": "",
    "settlementMonth": "",
    "securities": "",
    "submitOblgNm": "",
    "enterprise": "",
    "fromDate": frDate,
    "toDate": toDate,
    "reportNmTemp": "",
    "reportNmPop": "",
    "bfrDsclsType": "on",
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, data=data)
    # 현재 시간 가져오기
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # 파일 이름 생성
    file_name = f"tmp/list_page{pageIndex}_{timestamp}.html"

    # 파일에 저장
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(response.text)
    # 요청 결과 확인
    if response.status_code != 200:
        print(f"요청 실패! 상태 코드: {response.status_code}")
        return {}

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    # response.txt를 파일에 저장

    # 결과 저장용 리스트
    result_list = []

    # <tr> 태그 순회
    for tr in soup.find_all("tr"):
        # key 값 추출 (첫 번째 <td> 태그의 내용)
        key_td = tr.find("td", class_="first txc")
        if not key_td:
            continue
        key = key_td.get_text(strip=True)

        # <a href="#viewer"> 태그에서 title과 cd 추출
        a_tag = tr.find("a", href="#viewer")
        if a_tag:
            title = a_tag.get("title", "").strip()
            onclick_value = a_tag.get("onclick", "")

            # onclick에서 '20241220000050' 형식의 cd 값 추출
            if "openDisclsViewer" in onclick_value:
                cd_start = onclick_value.find("'") + 1
                cd_end = onclick_value.find("'", cd_start)
                cd = onclick_value[cd_start:cd_end]

        date_time_td = tr.find_all("td")[1]
        date_time = date_time_td.get_text(strip=True)

        company_name_td = tr.find_all("td")[2]
        company_name = company_name_td.get_text(strip=True)

        chechulin_td = tr.find_all("td")[4]  # <td>태그 중 5번째 (인덱스 4) 선택
        chechulin = chechulin_td.get_text(strip=True)
                # 리스트에 추가
        result_list.append({"key": key, "title": title, "cd": cd, "company_name": company_name, "date_time": date_time, "chechulin": chechulin})

    # 전체 건수와 페이지 수 추출
    total_count = 0
    total_page_count = 0

    # <div class="info type-00"> 태그 찾기
    info_div = soup.find("div", class_="info type-00")
    if info_div:
        # 전체 갯수 추출 (첫 번째 <em> 태그)
        total_count = int(info_div.find("em").get_text(strip=True).replace(",", ""))

        # 전체 페이지 수 추출 (텍스트에서 '/' 뒤의 숫자)
        import re
        match = re.search(r"/\s*(\d+)", info_div.get_text())
        total_page_count = int(match.group(1)) if match else 0

    # 최종 결과 반환
    return {
        "total_count": total_count,
        "total_page_count": total_page_count,
        "list": result_list,
    }

def fetchDetailWithSession(key, cd):
    """
    공시 상세 데이터를 세션을 사용하여 가져와 파일로 저장
    1. 최초 요청으로 세션 설정
    2. searchContents로 HTML 가져오기
    3. parent.setPath에서 최종 HTML URL 추출
    4. 최종 URL에서 HTML 가져오기
    """
    acptno = cd
    docno = cd
    session = requests.Session()  # 세션 유지
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    }
    
    # Step 2: searchContents 요청
    contents_url = f"https://kind.krx.co.kr/common/disclsviewer.do?method=searchContents&docNo={docno}"
    # headers["Referer"] = search_url  # Referer 헤더 추가
    response = session.get(contents_url, headers=headers)
    if response.status_code != 200:
        print(f"FAIL-{key} {cd} searchContents 요청 실패! 상태 코드: {response.status_code}")
        return

    # HTML 파싱 및 최종 URL 추출
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", string=re.compile("parent.setPath"))
    if not script_tag:
        print(f"FAIL-{key} {cd} parent.setPath를 찾을 수 없습니다.")
        return

    match = re.search(r"parent\.setPath\('.*?','(https://kind\.krx\.co\.kr/external/.*?)'", script_tag.string)
    if not match:
        print(f"FAIL-{key} 최종 URL을 추출할 수 없습니다.")
        return

    final_url = match.group(1)

    # Step 3: 최종 URL에서 HTML 가져오기
    final_response = session.get(final_url, headers=headers)
    if final_response.status_code != 200:
        print(f"FAIL-{key} 최종 URL 요청 실패! 상태 코드: {final_response.status_code}")
        return

    # UTF-8 변환 처리
    if final_response.encoding.lower() != "utf-8":
        final_response.encoding = "iso-8859-1"  # 서버 인코딩 명시
        content_utf8 = final_response.text.encode("iso-8859-1").decode("utf-8")
    else:
        content_utf8 = final_response.text

    # HTML 저장
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{key}.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content_utf8)

    print(f"SUCCESS-{key}-{cd} 상세 데이터가 {file_path}에 저장되었습니다.")


def fetch_iframe_content( key, cd, title):
    """
    Selenium을 사용하여 iframe 내용을 저장
    """
    # 브라우저 실행
    driver = get_driver()
    
    try:
        # Step 1: 메인 페이지 로드
        search_url = f"https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno={cd}&docno=&viewerhost=&viewerport="
        driver.get(search_url)

        # Step 2: <h1> 태그 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ttl.type-99.fleft"))
        )

        # Step 3: <h1> 태그 내용 추출
        h1_element = driver.find_element(By.CSS_SELECTOR, "h1.ttl.type-99.fleft")
        company_info = h1_element.text
        print(f"Extracted H1 Text: {company_info}")
        

        # Step 2: iframe 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#docViewFrm"))
        )
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe#docViewFrm")

        # Step 3: iframe 전환
        driver.switch_to.frame(iframe)

        # Step 4: iframe 내부 HTML 가져오기
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        iframe_content = driver.page_source

        # Step 5: 파일로 저장
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{key}.html"
        comment = f"<!-- title: {title} -->\n"
        comment = comment + f"<!-- company info: {company_info} -->\n"
        iframe_content = comment + iframe_content
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(iframe_content)

        print(f"SUCCESS-{key}-{cd}: iframe 내용이 {file_path}에 저장되었습니다.")
    except Exception as e:
        print(f"FAIL-{key}-{cd}: iframe 내용을 가져오는 중 오류 발생 - {e}")


def main(frdate, todate, page_index):
    """메인 함수"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if page_index == "all":
        page_index = 1
        all_results = []
        while True:
            data = getGoSiList(frdate, todate, page_index)
            if not data["list"]:
                break
            all_results.extend(data["list"])

            # fetchDetail 호출
            for item in data["list"]:
                # fetchDetailWithSession(item["key"], item["cd"])
                fetch_iframe_content(item["key"], item["cd"], item["title"])

            page_index += 1
            if page_index > data["total_page_count"]:
                break

        result_file_name = f"tmp/list_result_all_{timestamp}.txt"
        os.makedirs("tmp", exist_ok=True)
        with open(result_file_name, "w", encoding="utf-8") as result_file:
            result_file.write(str(all_results))
        print(f"전체 결과가 {result_file_name}에 저장되었습니다.")
    else:
        data = getGoSiList(frdate, todate, int(page_index))

        # fetchDetail 호출
        for item in data["list"]:
            # fetchDetailWithSession(item["key"], item["cd"])
            fetch_iframe_content(item["key"], item["cd"], item["title"])

        result_file_name = f"tmp/list_result_{page_index}_{timestamp}.txt"
        os.makedirs("tmp", exist_ok=True)
        with open(result_file_name, "w", encoding="utf-8") as result_file:
            result_file.write(str(data))
        print(f"페이지 {page_index} 결과가 {result_file_name}에 저장되었습니다.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("사용법: python kindscrap.py <frdate> <todate> <page_index>")
        print("\texample 1페이지: python kindscrap.py 2024-11-20 2024-12-20 1")
        print("\texample all: python kindscrap.py 2024-11-20 2024-12-20 all")
    else:
        frdate, todate, page_index = sys.argv[1], sys.argv[2], sys.argv[3]
        try:
            main(frdate, todate, page_index)
        finally:
            if driver:
                driver.quit()    
        # fetchDetailWithSession('1','20241219000947')