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

def get_url_and_tables(url:str, menu:str, sub_menu:str):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        # 메인 메뉴 클릭        
        xpath = f"//ul[@class='third-depth']//a[contains(text(), '{menu}')]"
        if not find_and_click_js(driver, xpath):
            print(f"{menu} 로 찾지 못함")
            return

        time.sleep(3)

        # ID가 '업종기간별추이'인 div 요소 찾기
        div_element = driver.find_element(By.ID, sub_menu)
        tr_cd_span = div_element.find_element(By.CSS_SELECTOR, 'span.apiCode')
        tr_cd = None
        if tr_cd_span: 
            tr_cd = tr_cd_span.text
            print(f"tr_cd: {tr_cd}")
        # 해당 div 하위의 클래스가 'btn btn-plus'인 버튼 요소 찾기
        button_element = div_element.find_element(By.CLASS_NAME, "btn-plus")
        button_element.click()
        print("버튼을 클릭했습니다.")

        time.sleep(3)
        # 페이지 소스를 가져와서 BeautifulSoup으로 파싱
        page_source = driver.page_source

        dataframes = {}
        soup = BeautifulSoup(page_source, 'html.parser')
        #기본정보 테이블들
        service_list_div = soup.find(id="service-list")
        title_div = service_list_div.find('div', class_='title-depth03')
        if title_div and title_div.find('h4', string='기본정보'):
            # 해당 div 다음에 있는 형제 요소 중 div를 찾기
            next_div = title_div.find_next_sibling('div')
            if next_div:
                html_div = StringIO(str(next_div))
                dataframes['기본정보'] = pd.read_html(html_div)[0]
            else:
                print("기본정보찾기 faile : 다음에 있는 div를 찾을 수 없습니다.")
        else:
            print("기본정보찾기 faile")        


        # ID가 각각 reqHeader, reqBody, resHeader, resBody인 div 요소 내의 테이블을 데이터프레임으로 변환
        ids = ["reqHeader", "reqBody", "resHeader", "resBody"]
        
        for div_id in ids:
            div_elements = soup.find_all(id=div_id)
            if div_elements:
                for div_element in div_elements:
                    table = div_element.find("table")
                    if table:
                        html_table_io = StringIO(str(table))
                        df = pd.read_html(html_table_io)[0]
                        dataframes[div_id] = df
                        print(f"{div_id} OK")
                        break
                    else:
                        print(f"{div_id} 안에 테이블이 없습니다.")
            else:
                print(f"{div_id}를 찾을 수 없습니다.")

        # for div_id in ids:
        #     div_element = soup.find_all(id=div_id)
        #     if div_element:
        #         print(f"div_element 내용:\n{div_element.prettify()}")  # div_element의 내용을 출력
        #         table = div_element.find("table")
        #         if table:
        #             html_table_io = StringIO(str(table))
        #             df = pd.read_html(html_table_io)[0]
        #             dataframes[div_id] = df
        #             print(f"{div_id} OK")
        #         else:
        #             print(f"{div_id} 안에 테이블이 없습니다.")
        #     else:
        #         print(f"{div_id}를 찾을 수 없습니다.")
    except TimeoutException :
        print("페이지 parsing 시간 초과")
        driver.quit()

    return tr_cd, dataframes

def json_pretty(json_str):
    try:
        data_dict = json.loads(json_str)
        s = json.dumps(data_dict, indent=4)
        return s
    except json.JSONDecodeError as e:
        return json_str

def write_basic_info(file, df):
    file.write("#기본정보\n")
    for i in range(len(df)):
        key = df.iloc[i, 0]
        value = df.iloc[i, 1]
        if key == 'URL':
            file.write(f'PATH = "{value}"\n')

def write_reqHeader_info(file, df, tr_cd):
    ''' reqHeader 정보를 파일에 쓰기'''
    file.write("\nheaders = {\n")
    for i in range(len(df)):
        key = df.iloc[i, 0]
        value = df.iloc[i, 1]
        desc = df.iloc[i,5]
        if key.lower() == 'authorization':
            file.write(f'\t"Authorization" : "Bearer " + ACCESS_TOKEN, \n')
        elif key.lower() == 'content-type':
            file.write(f'\t"Content-Type": "application/json; charset=utf-8",\n')
        elif key.lower() == 'tr_cd':
            file.write(f'\t"tr_cd" : "{tr_cd}", #{desc}\n')
        else:
            file.write(f'\t"{key}" : "{value}", #{desc}\n')
    file.write("}\n")

def write_reqBody_info(file, df, tr_cd):
    ''' reqBody 정보를 파일에 쓰기'''
    file.write("\ndata = {\n")
    inObject  = False
    for i in range(len(df)):
        key = df.iloc[i, 0]
        value = df.iloc[i, 1]
        typ = df.iloc[i, 2]
        desc = f"# {df.iloc[i,5]}" if df.iloc[i,5] != "" or df.iloc[i,5] != "nan"  else ""
        if key.startswith("-"):
            file.write(f'\t"{key[1:]}" : "{value}", {desc}\n')
        elif (typ.lower() == 'object' or typ.lower() == 'object array'):
            file.write(f'\t"{key}" : {{ \n')
            inObject = True

    if inObject:
        file.write("\t}\n")        
    file.write("}\n")

    file.write(f"\n\n#요청모델 데이터\n")
    file.write(f"class {tr_cd.upper()}_Request(StockApiBaseModel):\n")
    file.write(f"\ttr_cont: Optional[str] = 'N'\n")
    file.write(f"\ttr_cont_key: Optional[str] = ''\n")
    file.write(f"\tmac_address: Optional[str] = ''\n")
    for i in range(len(df)):
        key = df.iloc[i, 0]
        value = df.iloc[i, 1]
        typ = df.iloc[i, 2]
        length = df.iloc[i, 3]
        if typ.lower() == 'string':
            py_type = 'str'
        elif typ.lower() == 'number':
            py_type = 'int'
            if length.find('.') > 0:
                py_type = 'float'

        desc = f"{df.iloc[i,5]}"
        if desc == "" or desc == "nan":
            desc = ""

        if key.startswith("-"):
            file.write(f'\t{key[1:]} : {py_type} # {value} {desc}\n')
        elif (typ.lower() == 'object' or typ.lower() == 'object array'):
            file.write(f'\t{key} : {{ \n')
            inObject = True
    if inObject:
        file.write("\t}\n")        


def write_Res_Item(file, obj, df):
    ''' resBody 정보를 파일에 쓰기'''
    file.write(f"\nclass {obj['typeName']}(StockApiBaseModel):\n")
    isStart = False
    for i in range(len(df)):
        key = df.iloc[i, 0]
        name = df.iloc[i, 1]
        typ = df.iloc[i, 2]
        length_str = df.iloc[i, 4]
        desc = df.iloc[i,5]
        desc_str = f"{desc}"
        if desc_str == "nan":
            desc = ""
        if typ == 'String':
            py_type = 'str'
        elif typ == 'Number':
            py_type = 'int'
            if length_str.find('.') > 0:
                py_type = 'float'

        if key == obj['varName']:
            if (typ.lower() == 'object' or typ.lower() == 'object array') and key == obj['varName']:
                isStart = not isStart
        else:
            if isStart:
                file.write(f"\t{key[1:]}: {py_type} # {name} {desc if desc else ''}\n")

def write_resBody_info(file, df, tr_cd):
    ''' resBody 정보를 파일에 쓰기'''

    objects = []
    for i in range(len(df)):
        key = df.iloc[i, 0]
        typ = df.iloc[i, 2]
        if typ.lower() == 'object' or typ.lower() == 'object array':
            objects.append({"varName": key, "typeName": key.upper()})

    for obj in objects:
        write_Res_Item(file, obj, df)

    file.write(f"\nclass {tr_cd.upper()}_Response(StockApiBaseModel):\n")
    file.write(f"\trsp_cd: str\n")
    file.write(f"\trsp_msg: str\n")
    for obj in objects:
        file.write(f"\t{obj['varName']}: {obj['typeName']}\n")



def main(menu:str, sub_menu:str):
    driver = install_chrome_driver()
    url = "https://openapi.ls-sec.co.kr/apiservice?group_id=ffd2def7-a118-40f7-a0ab-cd4c6a538a90&api_id=33bd887a-6652-4209-88cd-5324bc7c5e36"
    tr_cd, dataframes = get_url_and_tables(url, menu,sub_menu= sub_menu)    
    #드라이버 종료
    driver.quit()

    # 데이터프레임 출력
    # with open("ls-doc.txt", "w", encoding="utf-8") as file:
    #     for key, df in dataframes.items():
    #         file.write(f"{key} 데이터프레임:\n")
    #         file.write(df.to_string())
    #         file.write("\n\n")
    filename = f"ls-{tr_cd}-{menu}-{sub_menu}.txt".replace("/", "_")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"#{menu}-{sub_menu}\n")
        write_basic_info(file, dataframes['기본정보'])
        write_reqHeader_info(file, dataframes['reqHeader'], tr_cd)
        write_reqBody_info(file, dataframes['reqBody'], tr_cd)
        write_resBody_info(file, dataframes['resBody'], tr_cd)

if __name__ == "__main__":

    menu = "[주식] 시세"
    sub_menu = "API용주식멀티현재가조회"
    main(menu, sub_menu)

    print("Done!")