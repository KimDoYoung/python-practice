# main.py
"""
모듈 설명: 
    - DART : https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=api_key 에서 xml다운로드 
    - 기존 ifi20 모두 삭제 후 저장
주요 기능:
    - https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=api_key 애서 xml 다운로드
    - 다운로드한 파일이 확장자가 xml이라도 그것이 zip파일 인지 판단
    - zip파일이라면 압축해제
    - xml 파싱
    - 현재 시간 보관
    - ifi20에 모두 저장
    - 저장 성공시 보관된 현재 시간을 기준으로 모두  ifi20 테이블 모두 삭제

작성자: 김도영
작성일: 2024-11-11
버전: 1.0
"""
import asyncio
import os
import aiohttp
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from sqlalchemy import func, insert, delete, select
from common.database import Database
from common.domain.ifi20_dart_corp_model import IFI20DartCorp  # SQLAlchemy ORM 모델 가정
from common.settings import config

# Open DART 인증키 (API key)
API_KEY = config.DART_API_KEY
API_URL = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API_KEY}"

# 한번에 일괄로 삽입할 데이터 수
BATCH_SIZE = 1000

DOWNLOAD_DIR = "data"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # 폴더가 없으면 생성

async def main():
    
    db = Database()
    # 기본 파일 경로
    file_path = os.path.join(DOWNLOAD_DIR, "corp_code_data.xml")

    # 1. 기존 file_path 파일이 존재하면 삭제
    if os.path.exists(file_path):
        os.remove(file_path)
    print(f"{file_path} 기존 파일 삭제 완료")    

    # 2. Open DART API에서 파일 다운로드 후 file_path로 저장
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            response.raise_for_status()
            content = await response.read()
    
    # 파일을 실제로 저장
    with open(file_path, "wb") as f:
        f.write(content)
    
    print(f"다운로드 완료: {file_path}")    

    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y_%m_%d_%H_%M_%S")


    # 3. 파일이 ZIP 파일이면 압축 해제 후 새 이름 지정
    if zipfile.is_zipfile(file_path):
        # ZIP 파일 해제 후 XML 파일명에 타임스탬프 추가
        with zipfile.ZipFile(file_path, "r") as zip_file:
            xml_filename = zip_file.namelist()[0]  # 첫 번째 XML 파일 가정
            extracted_xml_path = os.path.join(DOWNLOAD_DIR, f"corp_code_data_{today_str}.xml")
            zip_file.extract(xml_filename, DOWNLOAD_DIR)
            os.rename(os.path.join(DOWNLOAD_DIR, xml_filename), extracted_xml_path)
    else:
        # 4. XML 파일이면 바로 새 이름으로 저장
        extracted_xml_path = os.path.join(DOWNLOAD_DIR, f"corp_code_data_{today_str}.xml")
        os.rename(file_path, extracted_xml_path)

    # 5. XML 파일 파싱 및 데이터베이스에 일괄 저장
    data_iter = ET.iterparse(extracted_xml_path, events=("end",))
    records_to_insert = []
    insert_time = datetime.now(timezone.utc)
    print("데이터 저장 시작 : ", insert_time)
    async with db.get_connection() as session:
        for event, elem in data_iter:
            if elem.tag == "list":
                corp_code = elem.find("corp_code").text
                corp_name = elem.find("corp_name").text
                stock_code = elem.find("stock_code").text
                modify_date = elem.find("modify_date").text
                
                # stokc_code가 없으면 다음 레코드로 넘어감
                if stock_code.strip() == '':
                    continue

                # f_create_batchseq() 함수를 호출하여 ifi20_dart_corp_id 생성
                result = await session.execute(select(func.f_create_batchseq()))
                ifi20_dart_corp_id = result.scalar()  # 함수에서 반환된 ID 값


                records_to_insert.append({
                    "ifi20_dart_corp_id": ifi20_dart_corp_id,
                    "ifi20_corp_cd": corp_code,
                    "ifi20_corp_nm": corp_name,
                    "ifi20_stk_cd": stock_code,
                    "ifi20_modify_date": modify_date,
                    "ifi20_insert_time": datetime.now(timezone.utc)
                })

                # 일괄 삽입
                if len(records_to_insert) >= 1000:
                    await session.execute(insert(IFI20DartCorp).values(records_to_insert))
                    await session.commit()
                    records_to_insert = []

                elem.clear()  # 메모리에서 요소 제거

        # 남은 데이터 최종 삽입
        if records_to_insert:
            await session.execute(insert(IFI20DartCorp).values(records_to_insert))
            await session.commit()
        
        # insert_time보다 과거인 데이터 삭제
        await session.execute(delete(IFI20DartCorp).where(IFI20DartCorp.ifi20_insert_time < insert_time))
        await session.commit()

    print("ifi20 데이터 저장 및 이전 데이터 삭제 완료")

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("DART API 데이터 수집 시작: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("--------------------------------------------------")
    # asyncio.run(main())
    try:
        asyncio.run(main())
    except Exception as e:
        print("Error occurred:", e)    
    print("--------------------------------------------------")
    print("DART API 데이터 수집 종료: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("--------------------------------------------------")
