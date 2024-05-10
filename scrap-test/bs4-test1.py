import requests
from bs4 import BeautifulSoup
stock_code = '005930'
url = f'https://finance.naver.com/item/main.naver?code={stock_code}'
response = requests.get(url)
html_content = response.text

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')
# 투자의견 테이블 찾기
investment_table = soup.find("caption", string="투자의견").find_parent("table")

# 투자의견 테이블의 두 번째 행에서 <em> 태그를 찾음
values = investment_table.find_all("em")  # Assumes that all <em> in the second row are the target values

# 투자의견 테이블에서 추출한 값들을 리스트에 저장
values_extracted = [em.get_text() for em in values[2:4]] 
print(f'52주 최고, 최저: {values_extracted[0]}, {values_extracted[1]}')

# # 52주 최고/최저 값 추출하기
# # `52주최고`라는 텍스트를 포함하는 th 태그를 찾고, 이 태그의 다음 td 태그 내에서 <em> 태그를 찾음
# th_tag = soup.find('th', string=lambda text: text and '52주' in text)

# if th_tag:
#     td_tag = th_tag.find_next_sibling('td')
#     if td_tag:
#         em_tags = td_tag.find_all('em')
#         values_extracted = [em.text for em in em_tags]
#         print(f'52주 최고, 최저: {values_extracted[0]}, {values_extracted[1]}')
#     else:
#         print("td 태그를 찾을 수 없습니다.")
# else:
#     print("th 태그를 찾을 수 없습니다.")


