import time
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options

# 공모주 청약일정을 selenium을 사용하여 parsing 

chromedriver_autoinstaller.install()

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless 모드 활성화
chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model, 크롬의 일반적인 문제 해결 옵션
chrome_options.add_argument('--disable-dev-shm-usage')  # 컨테이너 환경에서 메모리 문제를 해결

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.38.co.kr/html/fund/index.htm?o=k'
driver.get(url)

# 페이지 로딩 대기
time.sleep(3)

# BeautifulSoup 객체로 웹 페이지의 HTML 분석
soup = BeautifulSoup(driver.page_source, 'html.parser')

# summary 속성이 "공모주 청약일정"인 테이블 찾기
table = soup.find('table', {'summary': '공모주 청약일정'})

# DataFrame으로 변환
df = pd.read_html(str(table))[0]

print(df)

# 드라이버 종료
driver.quit()