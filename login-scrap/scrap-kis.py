import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# 브라우저 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 1. 증권사 로그인 페이지 접속
url = 'https://securities.koreainvestment.com/main/member/login/login.jsp'
driver.get(url)

time.sleep(5)
# "ID로그인" 탭 클릭
tab_selector = '//div[@class="tab_content" and @data-tab="tab05"]'
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, tab_selector))
).click()

# 간편인증서 발급 안내 모달 창이 나타날 때까지 대기하다가 아니오 클릭
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'notBrowerCertPopup'))
)
no_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn_cancel' and contains(text(), '아니오')]"))
)
no_button.click()

# "ID로그인" 탭 클릭
tab_selector = '//div[@class="tab_content" and @data-tab="tab05"]'
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, tab_selector))
).click()

# 간편인증서 발급 안내 모달 창이 나타날 때까지 대기하다가 아니오 클릭
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'notBrowerCertPopup'))
)
no_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn_cancel' and contains(text(), '아니오')]"))
)
no_button.click()

# page source를  no_click_after.html로 저장
with open('no_click_after.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

id_login_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//li[@data-tab="id"]/a'))
)
id_login_tab.click()

#---------------------- 로그인
# # 3. ID와 비밀번호 입력을 위한 요소 대기
login_id = 'kdy8017'
login_pw = '8017kdy'

id_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'loginId'))
)
pw_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'loginPw'))
)

# ID와 비밀번호 입력 후 ENTER 키 입력
id_input.send_keys(login_id)
pw_input.send_keys(login_pw)
pw_input.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

#---------------------------------------
#  로그인 후에
# url = 'https://securities.koreainvestment.com/main/banking/inquiry/MyAsset.jsp'
# driver.get(url)

# page source를  no_click_after.html로 저장
# with open('no_click_after.html', 'w', encoding='utf-8') as f:
#     f.write(driver.page_source)


# 최근 접속정보 창이 나타날 때까지 대기하다가 닫기 버튼 클릭
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'loginInfo'))
)

# 닫기 버튼 찾기
close_button = driver.find_element(By.CSS_SELECTOR, '#loginInfo .btn_close')

# 닫기 버튼이 있는지 확인하고 클릭
if close_button:
    close_button.click()
    print("닫기 버튼을 클릭했습니다.")
else:
    print("닫기 버튼을 찾을 수 없습니다.")

# 현재 열려있는 모든 창의 핸들 목록 가져오기
main_window = driver.current_window_handle
all_windows = driver.window_handles

# 새로운 팝업 창이 열렸는지 확인
for window in all_windows:
    if window != main_window:
        # 새 창으로 전환
        driver.switch_to.window(window)
        print("팝업 창을 찾았습니다.")

        # 팝업 창 닫기
        driver.close()
        print("팝업 창을 닫았습니다.")

        # 원래 창으로 다시 전환
        driver.switch_to.window(main_window)
        print("원래 창으로 돌아왔습니다.")
url = 'https://securities.koreainvestment.com/main/banking/inquiry/MyAsset.jsp'
driver.get(url)
# 페이지 소스를 asset_page.html로 저장
with open('asset_page.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
    
try:
    # id="ctnt_data2" 요소를 찾음
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctnt_data2"))
    )

    # id="ctnt_data2" 안에서 id="radio01"인 라디오 버튼을 찾음
    radio_button = container.find_element(By.ID, "radio01")

    if radio_button:
        # 라디오 버튼이 화면에 보이도록 스크롤
        driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
        
        # JavaScript로 강제 클릭
        driver.execute_script("arguments[0].click();", radio_button)
        print("라디오 버튼을 클릭했습니다.")
        
        #time.sleep(5)  # 페이지가 로드될 때까지 대기
        # 기존의 테이블 (id='view01')이 갱신되기 전까지 기다림
        old_table = driver.find_element(By.ID, "view01")

        # 기존 테이블이 갱신(삭제 또는 업데이트)되기를 기다림
        WebDriverWait(driver, 10).until(EC.staleness_of(old_table))

        
        print('------------------------------------------------------------')
        print('전체계좌 조회를 수행합니다.')
        print('------------------------------------------------------------')            
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "view01"))  # 테이블이 페이지에 로드될 때까지 대기
        )
        
        # 테이블이 정상적으로 로드되면 HTML 출력
        print("테이블이 로드되었습니다.")
        table_html = table.get_attribute('outerHTML')
        #print(table_html)
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(table_html, 'html.parser')

        # 테이블의 데이터 추출
        rows = soup.find_all('tr')

        # 데이터 저장 리스트
        data = []
        columns = []

        # 헤더 추출 (첫 번째 row가 헤더)
        header = rows[0]
        for th in header.find_all('th'):
            columns.append(th.text.strip())  # 헤더를 리스트로 저장

        # 나머지 row에서 데이터 추출
        for row in rows[1:]:
            cells = row.find_all(['th', 'td'])  # th는 계좌번호, td는 데이터
            row_data = []
            for cell in cells:
                # 계좌번호의 경우 <a> 태그에서 값 추출
                if cell.find('a', class_='accountNum'):
                    row_data.append(cell.find('a', class_='accountNum').text.strip())
                else:
                    row_data.append(cell.text.strip())
            data.append(row_data)

        # Pandas DataFrame 생성
        df = pd.DataFrame(data, columns=columns)

        # DataFrame 출력
        print(df) 
        print('------------------------------------------------------------')
        print('result.csv 파일에 저장합니다')
        print('------------------------------------------------------------')            
        df.to_csv('result.csv', index=False, encoding='utf-8-sig')
        # 페이지 업데이트를 위한 대기
        #time.sleep(10)  # 서버에서 데이터를 받아오는 시간을 충분히 줌 (명시적 대기를 권장)
        
        # 페이지 소스 가져오기
        #page_source = driver.page_source
        
        # 페이지 소스에서 테이블 관련 정보 출력 (일단 텍스트로 확인)
        # page_source를 hidden_table.html로 저장
        #with open('hidden_table.html', 'w', encoding='utf-8') as f:
        #    f.write(page_source)
        
        # 로그아웃 버튼이 로드될 때까지 대기 (클래스 이름으로 찾기)
        print('------------------------------------------------------------')
        print('로그아웃을 수행합니다.')
        print('------------------------------------------------------------')
        logout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'btn_logout')]"))
        )
        # 로그아웃 버튼 강제로 클릭 
        driver.execute_script("arguments[0].click();", logout_button)
        # logout_button.click()
        print("로그아웃 버튼을 클릭했습니다.")        
        
        
    else:
        print("라디오 버튼을 찾을 수 없습니다.")

except Exception as e:
    print("오류 발생:", e)

print("기다렸다가.... 종료합니다....")
time.sleep(10)
driver.quit()
exit()








# time.sleep(10)
# driver.quit()
# exit()

# 간편인증서 발급 안내 모달 창이 나타날 때까지 대기하다가 아니오 클릭
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'notBrowerCertPopup'))
)
no_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn_cancel' and contains(text(), '아니오')]"))
)
no_button.click()






# # 6. 페이지 로딩 시간 대기
# time.sleep(5)

# # 7. 페이지 내용을 가져오기
page_source = driver.page_source
# page_source를 파일 1.html로 저장
with open('1.html', 'w', encoding='utf-8') as f:
    f.write(page_source)
print(page_source)
# 위페이지에는 내용이 없는데 팝업이 뜨는데 팝업의 소스를 가져와서 2.html에 저장


# 20초뒤에 브라우저 닫기
time.sleep(20)
driver.quit()
