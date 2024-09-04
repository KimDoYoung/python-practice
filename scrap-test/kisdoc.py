# kisdoc.py
"""
모듈 설명: 
    kis api document 를 scrapping해서 python code를 만든다.
    https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02-  
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

def find_and_click_js(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print(f"Error finding or clicking element with xpath '{xpath}': {e}")
        return False

def get_url_and_tables(url:str, main_menu:str, sub_menu:str):
    driver.get(url)
    # page_source = driver.page_source
    # with open("page_source.html", "w", encoding="utf-8") as f:
    #     f.write(page_source)
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        # # 대메뉴 클릭
        # main_menu_anchor = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, f"//span[text()='{main_menu}']"))
        # )
        # if main_menu_anchor is None:
        #     print(f"{main_menu} 로 찾지 못함")
        #     return None        
        # main_menu_anchor.click()

        # anchor = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, f"//span[text()='{sub_menu}']"))
        # )
        # anchor.click()
        # main_menu_xpath = f"//span[text()='{main_menu}']"
        # if not find_and_click_js(driver, main_menu_xpath):
        #     print(f"{main_menu} 로 찾지 못함")
        #     return
        
        sub_menu_xpath = f"//span[text()='{sub_menu}']"
        if not find_and_click_js(driver, sub_menu_xpath):
            print(f"{sub_menu} 로 찾지 못함")
            return


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

    return url, df_array, example_array

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

def maker_header_code(df):
    s = "{\n"
    for i in range(len(df)):
        element_name = df.loc[i, 'Element'].lower()
        required = df.loc[i, 'Required']
        desc = df.loc[i, 'Description']
        if required == 'Y':
            if element_name == "content-type" :
                s += f'"{element_name}": "{desc}",\n'
            elif element_name == "authorization":
                s += f'"{element_name}": f"Bearer {{self.ACCESS_TOKEN}}",\n'
            elif element_name == "appkey":
                s += f'"{element_name}": self.APP_KEY,\n'
            elif element_name == "appsecret":
                s += f'"{element_name}": self.APP_SECRET,\n'
            else:
                s += f'"{element_name}": "{desc}",\n'
    s += "}\n"
    return s

def maker_params_code(df, class_name):
    s = "{\n"

    for i in range(len(df)):
        element_name = df.loc[i, 'Element']
        required = df.loc[i, 'Required']
        han = df.loc[i, '한글명']
        desc = df.loc[i, 'Description']
        if required == 'Y':
            s += f'"{element_name}": "{han} {desc}",\n'
    s += "}\n"
    # class Request 
    s += f"class {class_name}_Request(StockApiBaseModel):\n"
    for i in range(len(df)):
        element_name = df.loc[i, 'Element']
        required = df.loc[i, 'Required']
        han = df.loc[i, '한글명']
        desc = df.loc[i, 'Description']
        _type = df.loc[i, 'Type']
        pytype = 'str'
        if _type != 'String':
            pytype = 'int'
        s += f'    {element_name}: {pytype} # {han} {desc}\n'

    return s

def item_script(df, class_name, ele_name):
    s = f"class {class_name}Item(StockApiBaseModel):\n"
    start : bool = False
    for i in range(len(df)):
        element_name = df.loc[i, 'Element']
        han_name = df.loc[i, '한글명']
        required = df.loc[i, 'Required']
        _type = 'str' if df.loc[i, 'Type'] == 'String' else df.loc[i, 'Type']
        desc = df.loc[i, 'Description']
        if element_name == ele_name:
            start = True
            continue
        if start:
            if element_name.startswith('-'):
                s += f'    {element_name[1:]}: str # {han_name} {desc}\n'
            elif  element_name.lower().startswith('output'):
                start = False
    return s
def make_pydantic_model(class_name, df):
    item_str= ""
    s = "from pydantic import BaseModel\n\n"
    s += f"class {class_name}_Response(StockApiBaseModel):\n"
    for i in range(len(df)):
        element_name = df.loc[i, 'Element']
        han_name = df.loc[i, '한글명']
        required = df.loc[i, 'Required']
        _type = 'str' if df.loc[i, 'Type'] == 'String' else df.loc[i, 'Type']
        desc = df.loc[i, 'Description']
        if required == 'Y':
            if element_name.startswith('-'):
                continue
            if element_name.lower().startswith('output'):
                item_str = item_script(df,class_name, element_name)
                if  df.loc[i, 'Type'] == 'Object' :
                    s += f'    {element_name}: {class_name}\n'
                    continue
                elif df.loc[i, 'Type'] == 'Array' :
                    s += f'    {element_name}: List[{class_name}Item]\n'
                    continue
            s += f'    {element_name}: {_type} # {han_name} {desc}\n'
    
    return_str = item_str + s
    
    return return_str

def main(main_menu:str, sub_menu:str):
    driver = install_chrome_driver()
    url = "https://apiportal.koreainvestment.com/apiservice/"
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
    class_name = ''.join([word.capitalize() for word in kis_path.split('-')])
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
        s = maker_header_code(request_header_df)
        f.write("heaer = \n")
        f.write(s)
        
        s = maker_params_code(request_query_df, class_name)
        f.write("params = \n")
        f.write(s)

        
        s = make_pydantic_model(class_name, response_body_df)
        f.write("pydantic model = \n")
        f.write(s)
        
        s = field_mapping_string(response_body_df)
        f.write(s)

    print(f"file write: {file_name} Done!")
    #드라이버 종료
    driver.quit()

if __name__ == "__main__":
    # main_menu  = "[국내주식] 종목정보"
    # sub_menu = "주식기본조회"
    
    # main_menu  = "[국내주식] 시세분석"
    # sub_menu = "종목조건검색조회"
    
    # main_menu  = "[국내주식] 종목정보"
    # sub_menu = "주식일별주문체결조회"

    # main_menu  = "[국내주식] 주문계좌"
    # sub_menu = "매도가능수량조회 "
    
    # main_menu  = "[국내주식] 업종/기타"
    # sub_menu = "국내휴장일조회"

    # main_menu  = "[국내주식] 순위분석"
    # sub_menu = "국내주식 시간외잔량 순위"

    # main_menu  = "[국내주식] 주문계좌"
    # sub_menu = "주식통합증거금 현황 "

    # main_menu  = "[국내주식] 시세분석"
    # sub_menu = "관심종목(멀티종목) 시세조회 "
    main_menu  = "[국내주식] 기본시세분석"
    sub_menu = "국내주식기간별시세(일/주/월/년)"

    main(main_menu, sub_menu)
    print("Done!")