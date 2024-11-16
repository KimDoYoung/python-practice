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
    - ifi20에 corp_cd로 있으면 updage 없으면 insert한다.
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
from sqlalchemy import func, insert, select, update
from common.database import Database
from common.domain.model.ifi20_dart_corp_model import IFI20DartCorp  # SQLAlchemy ORM 모델 가정
from common.settings import config
from common.utils import is_file_unchanged

# Open DART 인증키 (API key)
API_KEY = config.DART_API_KEY
API_URL = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={API_KEY}"

# 한번에 일괄로 삽입할 데이터 수
BATCH_SIZE = 1000

DOWNLOAD_DIR = config.DATA_FOLDER
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # 폴더가 없으면 생성
HASH_FILE = os.path.join(DOWNLOAD_DIR, "last_hash.txt")

async def main():
    
    db = Database()
    # 기본 파일 경로
    file_path = os.path.join(DOWNLOAD_DIR, "corp_code_data.xml")

    # 1. 기존 file_path 파일이 존재하면 삭제
    if os.path.exists(file_path):
        os.remove(file_path)
    print(f"기존 파일 삭제 : {file_path}")    

    # 2. Open DART API에서 파일 다운로드 후 file_path로 저장
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            response.raise_for_status()
            content = await response.read()
    
    # 파일을 실제로 저장
    with open(file_path, "wb") as f:
        f.write(content)
    
    print(f"다운로드 완료: {file_path}")
    
    # 3. 파일이 변경되지 않았으면 종료
    is_same_file = is_file_unchanged(file_path, HASH_FILE)
    if is_same_file:
        print("파일이 변경되지 않았습니다. 종료합니다.")
        return

    today = datetime.now(timezone.utc)
    today_str = today.strftime("%Y_%m_%d_%H_%M_%S")


    # 4. 파일이 ZIP 파일이면 압축 해제 후 새 이름 지정
    if zipfile.is_zipfile(file_path):
        # ZIP 파일 해제 후 XML 파일명에 타임스탬프 추가
        with zipfile.ZipFile(file_path, "r") as zip_file:
            xml_filename = zip_file.namelist()[0]  # 첫 번째 XML 파일 가정
            extracted_xml_path = os.path.join(DOWNLOAD_DIR, f"corp_code_data_{today_str}.xml")
            zip_file.extract(xml_filename, DOWNLOAD_DIR)
            os.rename(os.path.join(DOWNLOAD_DIR, xml_filename), extracted_xml_path)
            print(f"ZIP 파일 압축 해제: {extracted_xml_path}")
    else:
        # 4. XML 파일이면 바로 새 이름으로 저장
        extracted_xml_path = os.path.join(DOWNLOAD_DIR, f"corp_code_data_{today_str}.xml")
        os.rename(file_path, extracted_xml_path)

    # 5. XML 파일 파싱 및 데이터베이스에 일괄 저장
    data_iter = ET.iterparse(extracted_xml_path, events=("end",))
    records_to_insert = []
    insert_time = datetime.now(timezone.utc)
    print("ifi20에 저장 시작 : ", insert_time)
    async with db.get_connection() as session:
        for event, elem in data_iter:
            if elem.tag == "list":
                corp_code = elem.find("corp_code").text
                corp_name = elem.find("corp_name").text
                stock_code = elem.find("stock_code").text
                modify_date = elem.find("modify_date").text
                
                # f_create_batchseq() 함수를 호출하여 ifi20_dart_corp_id 생성
                result = await session.execute(select(func.f_create_batchseq()))
                ifi20_dart_corp_id = result.scalar()  # 함수에서 반환된 ID 값


                records_to_insert.append({
                    "ifi20_dart_corp_id": ifi20_dart_corp_id,
                    "ifi20_dart_corp_cd": corp_code,
                    "ifi20_dart_corp_nm": corp_name,
                    "ifi20_stk_cd": stock_code,
                    # "ifi20_modify_date": modify_date,
                    "ifi20_work_date": datetime.now(timezone.utc)
                })

                # 일괄 삽입
                if len(records_to_insert) >= 1000:
                    for record in records_to_insert:
                        existing_record = await session.execute(
                            select(IFI20DartCorp).where(IFI20DartCorp.ifi20_dart_corp_cd == record["ifi20_dart_corp_cd"])
                        )
                        existing_record = existing_record.scalar()
                        if existing_record:
                            await session.execute(
                                update(IFI20DartCorp)
                                .where(IFI20DartCorp.ifi20_dart_corp_cd == record["ifi20_dart_corp_cd"])
                                .values(record)
                            )
                        else:
                            await session.execute(insert(IFI20DartCorp).values(record))
                    await session.commit()
                    records_to_insert = []

                elem.clear()  # 메모리에서 요소 제거

        # 남은 데이터 최종 삽입
        if records_to_insert:
            for record in records_to_insert:
                existing_record = await session.execute(
                    select(IFI20DartCorp).where(IFI20DartCorp.ifi20_dart_corp_cd == record["ifi20_dart_corp_cd"])
                )
                existing_record = existing_record.scalar()
                if existing_record:
                    await session.execute(
                        update(IFI20DartCorp)
                        .where(IFI20DartCorp.ifi20_dart_corp_cd == record["ifi20_dart_corp_cd"])
                        .values(record)
                    )
                else:
                    await session.execute(insert(IFI20DartCorp).values(record))
            await session.commit()
        
    print("ifi20 데이터 저장 완료 : ", datetime.now(timezone.utc))

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
