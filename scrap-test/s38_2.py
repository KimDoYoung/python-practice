import time
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
from util import extract_dates, extract_numbers
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def insall_chrome_driver():
    chromedriver_autoinstaller.install()

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, 크롬의 일반적인 문제 해결 옵션
    chrome_options.add_argument('--disable-dev-shm-usage')  # 컨테이너 환경에서 메모리 문제를 해결

    global driver 
    driver = webdriver.Chrome(options=chrome_options)

def find_detail_url(table, stk_name):
    href = ""
    # 테이블 내 모든 행(tr)을 반복
    for tr in table.find_all('tr'):
        # 각 행에서 모든 'td' 태그 탐색
        for td in tr.find_all('td'):
            # 'td' 태그 내부의 'a' 태그를 찾고, 그 안에 있는 텍스트가 '엔젤로보틱스'인지 확인
            a_tag = td.find('a')
            if a_tag and stk_name in a_tag.get_text(strip=True):
                # 해당 'a' 태그의 'href' 속성 추출
                href = a_tag['href']
                #print(href)
                break

    return 'https://www.38.co.kr' + href
            
def get_ipo_list(url:str):
    driver.get(url)

    # 페이지 로딩 대기
    time.sleep(3)

    # BeautifulSoup 객체로 웹 페이지의 HTML 분석
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # summary 속성이 "공모주 청약일정"인 테이블 찾기
    table = soup.find('table', {'summary': '공모주 청약일정'})

    # DataFrame으로 변환
    df = pd.read_html(str(table))[0]

    #print(df)
    list = []
    for index, row in df.iterrows():
        stk_name = row.iloc[0]  # replace 0 with the index of the 'stk_name' column
        if str(stk_name) == 'nan':
            continue
        sub_sdate = row.iloc[1]
        start_ymd, end_ymd = extract_dates(row.iloc[1])  # replace 1 with the index of the 'sub_sdate' column
        final_offer_price = row.iloc[2]  # replace 2 with the index of the 'final_offer_price' column
        expect_price_range = row.iloc[3]  # replace 3 with the index of the 'expect_price_range' column
        start_cost, end_cost = extract_numbers(row.iloc[3])  # replace 3 with the index of the 'expect_price_range' column
        subscribe_rate = row.iloc[4]  # replace 4 with the index of the 'subscribe_rate' column
        lead_bookrunner = row.iloc[5]  # replace 5 with the index of the 'lead_bookrunner' column
        if final_offer_price == '-':
            detail_exists = False
        else:
            detail_exists = True
        detail_url = find_detail_url(table, stk_name)
        basic = {
            'stk_name': f"{stk_name}-{start_ymd}",
            'sub_dates': { "start": start_ymd, "end":end_ymd },
            'final_offer_price': final_offer_price,
            'expect_price_range': {"start" : start_cost, "end" : end_cost},
            'subscribe_rate': subscribe_rate,
            'lead_bookrunner': lead_bookrunner,
            'detail_exists': detail_exists,
            'detail_url': detail_url
        }
        list.append(basic)
        # print(basic)
    return list

def get_details(url: str):

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # summary 속성이 "기업개요"인 테이블 찾기
    table = soup.find('table', {'summary': '기업개요'})

    if not table:
        return {}  # 테이블이 없으면 빈 딕셔너리 반환

    company_info = {}
    # 정확히 두 칸을 넘어서 데이터를 읽기 위해 'td'를 직접 순회하지 않고 'tr'을 순회
    for tr in table.find_all('tr'):
        # 모든 'td' 요소를 찾아 리스트로 변환
        tds = tr.find_all('td')
        if not tds:
            continue

        # 각 'td' 요소의 텍스트를 읽고 해당 데이터를 사전에 저장
        for i in range(0, len(tds) - 1, 2):  # 한 행에 여러 데이터가 있을 수 있으므로 스텝을 2로 설정
            key = tds[i].get_text(strip=True)
            if key in ['종목명', '진행상황', '시장구분','종목코드','업종','대표자','본점소재지','홈페이지','최대주주',
                       '매출액','법인세비용차감전계속사업이익','순이익','자본금']:  # 필요한 키만 추출
                value = tds[i + 1].get_text(strip=True)
                company_info[key] = value

    # summary 속성이 "기업개요"인 테이블 찾기
    table = soup.find('table', {'summary': '공모정보'})
    
    if not table:
        return {}  # 테이블이 없으면 빈 딕셔너리 반환

    offering_info = {}
    # 정확히 두 칸을 넘어서 데이터를 읽기 위해 'td'를 직접 순회하지 않고 'tr'을 순회
    for tr in table.find_all('tr'):
        # 모든 'td' 요소를 찾아 리스트로 변환
        tds = tr.find_all('td')
        if not tds:
            continue

        # 각 'td' 요소의 텍스트를 읽고 해당 데이터를 사전에 저장
        for i in range(0, len(tds) - 1, 2):  # 한 행에 여러 데이터가 있을 수 있으므로 스텝을 2로 설정
            key = tds[i].get_text(strip=True)
            if key in ['총공모주식수','액면가','상장공모','희망공모가액','확정공모가','공모금액','주간사']: 
                value = tds[i + 1].get_text(strip=True)
                offering_info[key] = value


    table = soup.find('table', {'summary': '공모청약일정'})
    
    if not table:
        return {}  # 테이블이 없으면 빈 딕셔너리 반환

    schedule_info = {}
    # 정확히 두 칸을 넘어서 데이터를 읽기 위해 'td'를 직접 순회하지 않고 'tr'을 순회
    for tr in table.find_all('tr'):
        # 모든 'td' 요소를 찾아 리스트로 변환
        tds = tr.find_all('td')
        if not tds:
            continue

        # 각 'td' 요소의 텍스트를 읽고 해당 데이터를 사전에 저장
        for i in range(0, len(tds) - 1, 2):  # 한 행에 여러 데이터가 있을 수 있으므로 스텝을 2로 설정
            key = tds[i].get_text(strip=True)
            if key in ['수요예측일','공모청약일','납입일','환불일','상장일','IR일자','기관경쟁률','의무보유확약','신규상장일','현재가']: 
                value = tds[i + 1].get_text(strip=True)
                schedule_info[key] = value


    return { "company_info" : company_info, "offering_info" : offering_info ,"schedule_info" : schedule_info} 

def main():
    insall_chrome_driver()
    
    # urls = ['https://www.38.co.kr/html/fund/index.htm?o=k','https://www.38.co.kr/html/fund/index.htm?o=k&page=2']
    # for url in urls:
    #     list += get_ipo_list(url)
    # for basic in list:
        # get_ipo_detail(basic['detail_url'])
    detail = get_details('https://www.38.co.kr/html/fund/?o=v&no=2036&l=&page=1')
    print(detail)
    # 드라이버 종료
    driver.quit()


if __name__ == "__main__":
    main()


