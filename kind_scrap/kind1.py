import requests

# 요청 URL
url = "https://kind.krx.co.kr/disclosure/details.do"

# 헤더 설정 (개발자 도구에서 확인한 값을 참고)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}

# POST 데이터
data = {
    "method": "searchDetailsSub",
    "currentPageSize": 100,
    "pageIndex": 1,
    "orderMode": 1,
    "orderStat": "D",
    "forward": "details_sub",
    "disclosureType01": "",
    "disclosureType02": "",
    "disclosureType03": "",
    "disclosureType04": "",
    "disclosureType05": "",
    "disclosureType06": "",
    "disclosureType07": "",
    "disclosureType08": "",
    "disclosureType09": "",
    "disclosureType10": "",
    "disclosureType11": "",
    "disclosureType13": "",
    "disclosureType14": "",
    "disclosureType20": "",
    "pDisclosureType01": "",
    "pDisclosureType02": "",
    "pDisclosureType03": "",
    "pDisclosureType04": "",
    "pDisclosureType05": "",
    "pDisclosureType06": "",
    "pDisclosureType07": "",
    "pDisclosureType08": "",
    "pDisclosureType09": "",
    "pDisclosureType10": "",
    "pDisclosureType11": "",
    "pDisclosureType13": "",
    "pDisclosureType14": "",
    "pDisclosureType20": "",
    "searchCodeType": "",
    "repIsuSrtCd": "",
    "allRepIsuSrtCd": "",
    "oldSearchCorpName": "",
    "disclosureType": "",
    "disTypevalue": "",
    "reportNm": "",
    "reportCd": "",
    "searchCorpName": "",
    "business": "",
    "marketType": "",
    "settlementMonth": "",
    "securities": "",
    "submitOblgNm": "",
    "enterprise": "",
    "fromDate": "2024-11-20",
    "toDate": "2024-12-20",
    "reportNmTemp": "",
    "reportNmPop": "",
    "bfrDsclsType": "on",
}


# POST 요청 보내기
response = requests.post(url, headers=headers, data=data)

# 응답 확인
if response.status_code == 200:
    print("응답 성공!")
    print(response.text)  # 응답 본문 출력
    with open("response.html", "w", encoding="utf-8") as file:
        file.write(response.text)
        
else:
    print(f"요청 실패! 상태 코드: {response.status_code}")
