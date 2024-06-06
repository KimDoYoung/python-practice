# kisdoc.py
"""
모듈 설명: 
    https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02-  [kis api](https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02) 를 scrapping해서 python code를 만든다.
주요 기능:
    - kis api를 selenium을 이용하여 scrapping
    - path에 따른 request/response를 해석해서 python code를 만든다.

작성자: 김도영
작성일: 06
버전: 1.0
"""
from io import StringIO
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.common.exceptions import TimeoutException
import pandas as pd

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

def find_url(parent_div):
    div_tag = parent_div.find('div', string='URL')

    # 그 부모 <li> 요소 찾기
    li_tag = div_tag.find_parent('li') if div_tag else None

    # 부모 <li> 요소의 형제 <span> 요소 찾기
    span_tag = li_tag.find('span') if li_tag else None

    # 형제 <span> 요소의 텍스트 추출
    span_text = span_tag.get_text(strip=True) if span_tag else None    
    return span_text

def get_url_and_tables(url:str, main_menu:str, sub_menu:str):
    driver.get(url)
    
    try:
        # 대메뉴 클릭
        main_menu_anchor = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{main_menu}']"))
        )
        if main_menu_anchor is None:
            print(f"{main_menu} 로 찾지 못함")
            return None        
        main_menu_anchor.click()

        #  api 주제를 클릭
        sub_menu_anchor = driver.find_element(By.XPATH, f"//span[text()='{sub_menu}']/parent::a")
        if sub_menu_anchor is None:
            print(f"{sub_menu} 로 찾지 못함")
            return None
        sub_menu_anchor.click()

        # 페이지가 로드될 때까지 대기
        # element_present = EC.presence_of_element_located((By.ID, 'kis-list'))
        # WebDriverWait(driver, 10).until(element_present)

        time.sleep(5)

        # 페이지 소스를 가져와서 BeautifulSoup으로 파싱
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # title이 "주식잔고조회"  일 때<h2> 태그 찾기
        h2_tag = soup.find('h2', string=lambda t: t and sub_menu in t)

        # 해당 <h2> 태그의 부모 <div> 요소 찾기
        parent_div = h2_tag.find_parent('div')

        #URL찾기
        # "URL" 텍스트를 가진 <div> 요소 찾기
        url = find_url(parent_div)

        # 테이블 4개 찾기
        tables = parent_div.find_all('table')
        
        df_array = []

        for table in tables:
            # table을 pandas의 DataFrame으로 변환
            df = pd.read_html(StringIO(str(table)))[0]
            df_array.append(df)
        # Example 찾기
        example_div_parent = parent_div.find('div', class_='api_example_wrap')
        example_divs = example_div_parent.find_all('div', class_='example_apicode_box')
        example_array = []
        for example_div in example_divs:
            example_code = example_div.get_text(strip=True)
            example_array.append(example_code)

    except TimeoutException :
        print("페이지 parsing 시간 초과")
        driver.quit()

    return url, df_array , example_array

def field_mapping_string(df):
    s = ""
    for i in range(len(df)):
        element_name = df.loc[i, 'Element']
        if element_name.startswith('-'):
            # Element          한글명    Type Required  Length                                        Description
            s += f'FieldMapping(Element="{df.loc[i, "Element"][1:]}", 한글명="{df.loc[i, "한글명"]}", Type="{df.loc[i, "Type"]}", Required="{df.loc[i, "Required"]}", Length={df.loc[i, "Length"]}, Description="{df.loc[i, "Description"]}"),\n'
    return s

def json_pretty(json_str):
    try:
        data_dict = json.loads(json_str)
        s = json.dumps(data_dict, indent=4)
        return s
    except json.JSONDecodeError as e:
        return json_str


def main(main_menu:str, sub_menu:str):
    driver = install_chrome_driver()
    url = "https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02"
    url, df_array, example_array = get_url_and_tables(url, main_menu, sub_menu)
    print(f"url: {url}")
    request_header_df = df_array[0]
    request_query_df = df_array[1]
    response_header_df = df_array[2]
    response_body_df = df_array[3]
    request_example = example_array[0]
    response_example = example_array[1]

    response_body_df['Description'] = response_body_df['Description'].fillna('')
    response_body_df['Length'] = response_body_df['Length'].fillna(0).astype(int)

    #파일에 write
    kis_path =  url.split('/')[-1]
    file_name = f"kis_{kis_path}.txt"
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(f"url: {url}\n")
        f.write("Request Header\n")
        f.write(request_header_df.to_string())
        f.write("\n\nRequest Query\n")
        f.write(request_query_df.to_string())
        f.write("\n\nResponse Header\n")
        f.write(response_header_df.to_string())
        f.write("\n\nResponse Body\n")
        f.write(response_body_df.to_string())

        f.write("\n\nRequest Example\n")
        s = json_pretty(request_example)
        f.write(s)
        f.write("\n\nResponse Example\n")
        s = json_pretty(response_example)
        f.write(s)
        f.write("\n---------------------------------\n")
        s = field_mapping_string(response_body_df)
        f.write(s)

    print(f"file write: {file_name} Done!")
    #드라이버 종료
    driver.quit()

if __name__ == "__main__":
    main_menu  = "[국내주식] 주문/계좌"
    sub_menu = "주식잔고조회"
    main(main_menu, sub_menu)