import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# 경고 무시 설정
warnings.simplefilter('ignore', InsecureRequestWarning)

# 요청할 URL
url = 'https://openapi.ls-sec.co.kr/apiservice?group_id=ffd2def7-a118-40f7-a0ab-cd4c6a538a90&api_id=33bd887a-6652-4209-88cd-5324bc7c5e36'

# 요청 보내기
response = requests.get(url, verify=False)

# 요청이 성공했는지 확인
if response.status_code == 200:
    # 응답 내용을 파일에 저장
    with open('lsdoc1.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("응답 내용이 'lsdoc1.html' 파일에 저장되었습니다.")
else:
    print(f"요청이 실패했습니다. 상태 코드: {response.status_code}")
