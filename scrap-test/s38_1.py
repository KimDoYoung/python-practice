import urllib3
from urllib3.util.ssl_ import create_urllib3_context
from bs4 import BeautifulSoup
import pandas as pd
import ssl

# SSL 컨텍스트 생성 및 TLS 1.3 활성화
ctx = create_urllib3_context()
ctx.options |= ssl.OP_NO_SSLv2
ctx.options |= ssl.OP_NO_SSLv3
ctx.options |= ssl.OP_NO_TLSv1
ctx.options |= ssl.OP_NO_TLSv1_1
ctx.options |= ssl.OP_NO_TLSv1_2

# PoolManager를 사용하여 커스텀 SSL 컨텍스트 적용
http = urllib3.PoolManager(ssl_context=ctx)
url = 'https://www.38.co.kr/html/fund/index.htm?o=k'
response = http.request('GET', url)
html = response.data.decode('utf-8')

# BeautifulSoup 객체를 생성합니다.
soup = BeautifulSoup(html, 'html.parser')

# summary 속성이 "공모주 청약일정"인 테이블을 찾습니다.
table = soup.find('table', {'summary': '공모주 청약일정'})

# pandas의 read_html 함수를 사용하여 HTML 테이블을 DataFrame으로 변환합니다.
dfs = pd.read_html(str(table))

# DataFrame 리스트 중 첫 번째 DataFrame을 가져옵니다.
df = dfs[0]
print(df)
