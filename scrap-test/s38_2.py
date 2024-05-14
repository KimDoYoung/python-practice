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

def install_chrome_driver():
    chromedriver_autoinstaller.install()

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, 크롬의 일반적인 문제 해결 옵션
    chrome_options.add_argument('--disable-dev-shm-usage')  # 컨테이너 환경에서 메모리 문제를 해결

    global driver 
    driver = webdriver.Chrome(options=chrome_options)
    return driver

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

    soup = get_soup(url);
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
            fixed = False
        else:
            fixed = True
        detail_url = find_detail_url(table, stk_name)
        basic = {
            'stk_name': f"{stk_name}-{start_ymd}",
            'sub_dates': { "start": start_ymd, "end":end_ymd },
            'final_offer_price': final_offer_price,
            'expect_price_range': {"start" : start_cost, "end" : end_cost},
            'subscribe_rate': subscribe_rate,
            'lead_bookrunner': lead_bookrunner,
            'fixed': fixed,
            'detail_url': detail_url,
            'details' : {}
        }
        list.append(basic)
        # print(basic)
    return list


def get_soup(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
    return BeautifulSoup(driver.page_source, 'html.parser')

def find_table_by_summary(soup, summary):
    table = soup.find('table', {'summary': summary})
    if not table:
        return None
    return table

def extract_company_info(soup):
    data = {}
    table = find_table_by_summary(soup, '기업개요') 

    if not table:
        return data  # 테이블이 없으면 빈 딕셔너리 반환
    
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if not tds:
            continue
        for i in range(0, len(tds) - 1, 2):  # 한 행에 여러 데이터가 있을 수 있으므로 스텝을 2로 설정
            key = tds[i].get_text(strip=True)
            if key in ['종목명', '진행상황', '시장구분','종목코드','업종','대표자','본점소재지','홈페이지','최대주주',
                        '매출액','법인세비용차감전계속사업이익','순이익','자본금']:  # 필요한 키만 추출
                value = tds[i + 1].get_text(strip=True)
                data[key] = value
    return data

def extract_offering_info(soup):
    data = {}
    table = find_table_by_summary(soup, '공모정보') 
    
    if not table:
        return data  # 테이블이 없으면 빈 딕셔너리 반환

    for tr in table.find_all('tr'):
        # 모든 'td' 요소를 찾아 리스트로 변환
        tds = tr.find_all('td')
        if not tds:
            continue

        for i in range(0, len(tds) - 1, 2):  # 한 행에 여러 데이터가 있을 수 있으므로 스텝을 2로 설정
            key = tds[i].get_text(strip=True)
            if key in ['총공모주식수','액면가','상장공모','희망공모가액','확정공모가','공모금액','주간사']: 
                value = tds[i + 1].get_text(strip=True)
                data[key] = value
    return data

def extract_schedule_info(soup):
    data = {}
    table = find_table_by_summary(soup, '공모청약일정') 
    
    if not table:
        return data  # 테이블이 없으면 빈 딕셔너리 반환

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
                data[key] = value.replace('\xa0', '')
    return data

def extract_expected_participation(soup):
    target_td = soup.find('td', string='참여건수 (단위:건)')
    if not target_td:
        return {}
    target_tr = target_td.find_parent('tr')
    data_tr = target_tr.find_next_sibling('tr')
    data_tds = data_tr.find_all('td')
    data = [td.get_text() for td in data_tds]
    expected_participation = {}
    expected_participation['참여건수'] = data[0]
    expected_participation['신청주식수'] = data[1]
    expected_participation['단순경쟁'] = data[2]
    return expected_participation

def extract_nav_per_share(soup):
    td = soup.find('td', string=lambda x: x and "무형자산 등 차감" in x)
    if td is None:
        return {}
    target_table = td.find_parent('table')
    rows = target_table.find_all('tr')
    # 결과를 저장할 딕셔너리
    nav_per_share = {}

    # 각 <tr> 요소에서 첫 번째 <td>와 두 번째 <td>의 텍스트 추출
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            nav_per_share[key] = value    
    return nav_per_share

def extract_earnings_value_per_share(soup):
    '''본질가치 평가 - 주당 수익가치'''
    td = soup.find('td', string=lambda x: x and "주당 이익(EPS)" in x)
    if td is None:
        return {}
    table = td.find_parent('table')

    # 결과를 저장할 딕셔너리
    earnings_value_per_share = {}

    # 테이블 내 모든 <tr> 요소 추출
    rows = table.find_all('tr')

    # 첫 번째 행(헤더)에서 연도 정보 추출
    header = rows[0].find_all('td')
    years = [header[i].get_text(strip=True) for i in range(1, len(header))]

    # 나머지 행들에서 데이터 추출
    for row in rows[1:]:
        cols = row.find_all('td')
        key = cols[0].get_text(strip=True)
        values = [col.get_text(strip=True) for col in cols[1:]]
        if key in ["가중평균 EPS", "자본환원율(%)", "수익가치 (평가법 1)"]:
            # 단일 값을 가지는 항목 처리
            earnings_value_per_share[key] = values[0]
        else:
            # 연도별 값을 가지는 항목 처리
            earnings_value_per_share[key] = {year: value for year, value in zip(years, values)}

    return earnings_value_per_share

def extract_intrinsic_value_per_share(soup):
    ''' 주당 본질 가치 평가 '''
    intrinsic_value_per_share = {} 
    td = soup.find('td', string=lambda x: x and "1주당 금액" in x)
    if td is None:
        return {}
    table = td.find_parent('table')
    rows = table.find_all('tr')

    # 헤더 추출
    header = rows[0].find_all('td')
    columns = [col.get_text(strip=True) for col in header[1:]]

    # 나머지 행들에서 데이터 추출
    for row in rows[1:]:
        cols = row.find_all('td')
        key = cols[0].get_text(strip=True)
        values = [col.get_text(strip=True) for col in cols[1:]]
        
        if len(values) == 1:  # "본질가치 (평가법 1)" 항목의 경우
            intrinsic_value_per_share[key] = values[0]
        else:
            intrinsic_value_per_share[key] = {columns[i]: values[i] for i in range(len(values))}
    return intrinsic_value_per_share

def extract_financial_ratio(soup):
    financial_ratio = {}
    td = soup.find('td', string=lambda x: x and "영업이익증가율" in x)
    if td is None:
        return {}
    table = td.find_parent('table')
    first_row = table.find('tr')
    # 첫 번째 행의 모든 'td' 요소를 찾습니다
    tds = first_row.find_all('td')

    # 첫 번째 행에 4개의 'td' 요소가 있는지 확인합니다
    if len(tds) != 4:
        return {}
# 테이블 내 모든 <tr> 요소 추출
    rows = table.find_all('tr')

    # 첫 번째 행(헤더)에서 연도 정보 추출
    header = rows[0].find_all('td')
    years = [header[i].get_text(strip=True) for i in range(2, len(header))]

    # 나머지 행들에서 데이터 추출
    current_category = None
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols[0].get('rowspan'):
            current_category = cols[0].get_text(strip=True)
        key = cols[1].get_text(strip=True)
        values = [col.get_text(strip=True).replace('&nbsp;', '') for col in cols[2:]]
        if current_category not in financial_ratio:
            financial_ratio[current_category] = {}
        financial_ratio[current_category][key] = {year: value for year, value in zip(years, values)}
    
    return financial_ratio

def extract_stock_price_indicators(soup):
    stock_price_indicators = {}
    font = soup.find('font', string='PER')
    if font is None:
        return {}
    
    table = font.find_parent('table')

# 테이블 내 모든 <tr> 요소 추출
    rows = table.find_all('tr')

    # 첫 번째 행(헤더)에서 연도 정보 추출
    header = rows[0].find_all('td')
    years = [header[i].get_text(strip=True) for i in range(1, len(header))]

    # 나머지 행들에서 데이터 추출
    for row in rows[1:]:
        cols = row.find_all('td')
        key = cols[0].get_text(strip=True).replace('&nbsp;', '')
        values = [col.get_text(strip=True).replace('&nbsp;', '').replace(' 원', '') for col in cols[1:]]
        stock_price_indicators[key] = {year: value for year, value in zip(years, values)}

    return stock_price_indicators

def extract_over_markte_price(soup):
    td = soup.find('td', string=lambda x: x and "팝니다 (가격참고)" in x)
    if td is None:
        return {}
    table = td.find_parent('table')    
    rows = table.find_all('tr')[1:]  # 첫 번째 행은 헤더라고 가정하고 제외


    over_markte_price = {"seller":[],"buyer":[]}

    for index, row in enumerate(rows):
        cols = row.find_all('td')
        product_name = cols[0].text.strip()
        product_name = product_name.split('\n')[-1].strip() if '\n' in product_name else product_name  # 더 안전한 제품 이름 추출
        over_markte_price["seller"].append({
            "product": product_name,
            "price": cols[1].text.strip(),
            "quantity": cols[2].text.strip(),
            "date": cols[3].text.strip()
        })

    td = soup.find('td', string=lambda x: x and "삽니다 (가격참고)" in x)
    table = td.find_parent('table')    
    rows = table.find_all('tr')[1:]  # 첫 번째 행은 헤더라고 가정하고 제외

    for index, row in enumerate(rows):
        cols = row.find_all('td')
        product_name = cols[0].text.strip()
        product_name = product_name.split('\n')[-1].strip() if '\n' in product_name else product_name  # 더 안전한 제품 이름 추출
        over_markte_price["buyer"].append({
            "product": product_name,
            "price": cols[1].text.strip(),
            "quantity": cols[2].text.strip(),
            "date": cols[3].text.strip()
        })
    return over_markte_price

def get_details(url: str):

    soup = get_soup(url)
    company_info = extract_company_info(soup)
    offering_info = extract_offering_info(soup)
    schedule_info = extract_schedule_info(soup)

    # 수요예측 참여건수
    expected_participation = extract_expected_participation(soup)

    # 본질가치 평가 - 주당 순자산가치 평가
    nav_per_share = extract_nav_per_share(soup)
    
    # 본질가치 평가 - 주당 수익가치
    earnings_value_per_share = extract_earnings_value_per_share(soup)

    # 주당 본질 가치 평가
    intrinsic_value_per_share = extract_intrinsic_value_per_share(soup)

    # 재무비율
    financial_ratio = extract_financial_ratio(soup)

    #주가 지표
    stock_price_indicators = extract_stock_price_indicators(soup)

    # 장외시장 가격
    over_markte_price = extract_over_markte_price(soup)

    return { "company_info" : company_info, "offering_info" : offering_info ,
            "schedule_info" : schedule_info, "expected_participation" : expected_participation,
            "nav_per_share" : nav_per_share, "earnings_value_per_share" : earnings_value_per_share, 
            "intrinsic_value_per_share" : intrinsic_value_per_share,
            "financial_ratio" : financial_ratio, "stock_price_indicators" : stock_price_indicators,
            "over_markte_price": over_markte_price} 

def main():
    driver = install_chrome_driver()
    
    urls = ['https://www.38.co.kr/html/fund/index.htm?o=k','https://www.38.co.kr/html/fund/index.htm?o=k&page=2']
    #urls = ['https://www.38.co.kr/html/fund/index.htm?o=k&page=2']
    #urls = ['https://www.38.co.kr/html/fund/index.htm?o=k']
    list = []
    for url in urls:
        list = get_ipo_list(url)
        for basic in list:
            detail = get_details(basic['detail_url'])
            basic['details'] = detail
            print(basic)
            time.sleep(1)    
    # print(list)
    # for basic in list:
    #     detail = get_details('https://www.38.co.kr/html/fund/?o=v&no=2036&l=&page=1')
    # print(detail)
    # 드라이버 종료
    driver.quit()


if __name__ == "__main__":
    main()


