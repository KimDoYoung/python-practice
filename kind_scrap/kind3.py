import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def getGoSiList(frDate, toDate, pageIndex):
    # 요청 URL 및 헤더 설정
    url = "https://kind.krx.co.kr/disclosure/details.do"
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
    "fromDate": frDate,
    "toDate": toDate,
    "reportNmTemp": "",
    "reportNmPop": "",
    "bfrDsclsType": "on",
    }

    # POST 요청 보내기
    response = requests.post(url, headers=headers, data=data)
    # 현재 시간 가져오기
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # 파일 이름 생성
    file_name = f"tmp/list_page{pageIndex}_{timestamp}.html"

    # 파일에 저장
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(response.text)
    # 요청 결과 확인
    if response.status_code != 200:
        print(f"요청 실패! 상태 코드: {response.status_code}")
        return {}

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    # response.txt를 파일에 저장

    # 결과 저장용 리스트
    result_list = []

    # <tr> 태그 순회
    for tr in soup.find_all("tr"):
        # key 값 추출 (첫 번째 <td> 태그의 내용)
        key_td = tr.find("td", class_="first txc")
        if not key_td:
            continue
        key = key_td.get_text(strip=True)

        # <a href="#viewer"> 태그에서 title과 cd 추출
        a_tag = tr.find("a", href="#viewer")
        if a_tag:
            title = a_tag.get("title", "").strip()
            onclick_value = a_tag.get("onclick", "")

            # onclick에서 '20241220000050' 형식의 cd 값 추출
            if "openDisclsViewer" in onclick_value:
                cd_start = onclick_value.find("'") + 1
                cd_end = onclick_value.find("'", cd_start)
                cd = onclick_value[cd_start:cd_end]

                # 리스트에 추가
                result_list.append({"key": key, "title": title, "cd": cd})

    # 전체 건수와 페이지 수 추출
    total_count = 0
    total_page_count = 0

    # <div class="info type-00"> 태그 찾기
    info_div = soup.find("div", class_="info type-00")
    if info_div:
        # 전체 갯수 추출 (첫 번째 <em> 태그)
        total_count = int(info_div.find("em").get_text(strip=True).replace(",", ""))

        # 전체 페이지 수 추출 (텍스트에서 '/' 뒤의 숫자)
        import re
        match = re.search(r"/\s*(\d+)", info_div.get_text())
        total_page_count = int(match.group(1)) if match else 0

    # 최종 결과 반환
    return {
        "total_count": total_count,
        "total_page_count": total_page_count,
        "list": result_list,
    }

def fetchDetail(key, cd):
    """공시 상세 데이터를 가져와 파일로 저장"""
    url = f"https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno={cd}&docno=&viewerhost=&viewerport="
    response = requests.get(url)
    if response.status_code != 200:
        print(f"FAIL-{key} 요청 실패! 상태 코드: {response.status_code}")
        return

    # HTML 저장
    soup = BeautifulSoup(response.text, "html.parser")
    xforms_div = soup.find("div", class_="xforms")
    if not xforms_div:
        print("FAIL-{key} xforms 데이터를 찾을 수 없습니다.")
        return

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{key}.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xforms_div.decode())
    print(f"{key} {cd} 상세 데이터가 {file_path}에 저장되었습니다.")

def main(frdate, todate, page_index):
    """메인 함수"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    if page_index == "all":
        page_index = 1
        all_results = []
        while True:
            data = getGoSiList(frdate, todate, page_index)
            if not data["list"]:
                break
            all_results.extend(data["list"])

            # fetchDetail 호출
            for item in data["list"]:
                fetchDetail(item["key"], item["cd"])

            page_index += 1
            if page_index > data["total_page_count"]:
                break

        result_file_name = f"tmp/list_result_all_{timestamp}.txt"
        os.makedirs("tmp", exist_ok=True)
        with open(result_file_name, "w", encoding="utf-8") as result_file:
            result_file.write(str(all_results))
        print(f"전체 결과가 {result_file_name}에 저장되었습니다.")
    else:
        data = getGoSiList(frdate, todate, int(page_index))

        # fetchDetail 호출
        for item in data["list"]:
            fetchDetail(item["key"], item["cd"])

        result_file_name = f"tmp/list_result_{page_index}_{timestamp}.txt"
        os.makedirs("tmp", exist_ok=True)
        with open(result_file_name, "w", encoding="utf-8") as result_file:
            result_file.write(str(data))
        print(f"페이지 {page_index} 결과가 {result_file_name}에 저장되었습니다.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("사용법: python kindscrap.py <frdate> <todate> <page_index>")
    else:
        frdate, todate, page_index = sys.argv[1], sys.argv[2], sys.argv[3]
        main(frdate, todate, page_index)