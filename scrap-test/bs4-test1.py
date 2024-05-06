import requests
from bs4 import BeautifulSoup

url = 'https://www.tfreeca22.com/board.php?mode=list&b_id=tdrama'
response = requests.get(url)
html_content = response.text

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# 클래스가 'b_list'인 테이블 찾기
table = soup.find('table', class_='b_list')
anchors = table.find_all('a') if table else []

# 각 앵커의 href 속성과 텍스트 출력
for a in anchors:
    print(f'URL: {a["href"]}, Text: {a.text}')