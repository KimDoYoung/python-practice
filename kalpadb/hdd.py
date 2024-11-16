import os
import sys
import pymysql
import datetime
from dotenv import load_dotenv

from kalpadb_utils import generate_srch_key

# .env 파일 로드
load_dotenv()

# DB 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),  # 기본 포트 3306
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')  # 기본 문자셋 utf8mb4
}

def get_initial_id(cursor):
    """현재 최대 ID 값을 조회"""
    cursor.execute("SELECT MAX(id) + 1 FROM hdd")
    result = cursor.fetchone()
    return result[0] if result[0] else 1

def insert_to_db(cursor, data):
    """hdd 테이블에 데이터 삽입"""
    query = """
        INSERT INTO hdd (id, volumn_name, gubun, path, file_name, name, pdir, extension, size, sha1_cd, srch_key, last_modified_ymd, pid, right_pid)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)

def scan_directory(root_path, volume_name):
    """디렉터리를 순회하며 데이터를 DB에 삽입"""
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        # 처음에 최대 ID를 가져오고 이후엔 프로그램 내에서 관리
        current_id = get_initial_id(cursor)
        parent_pid = None  # 부모 폴더 ID 초기값

        for current_path, dirs, files in os.walk(root_path):
            # 부모 디렉터리 이름
            parent_dir_name = os.path.basename(os.path.dirname(current_path))

            # 디렉터리 처리
            for dir_name in dirs:
                full_path = os.path.join(current_path, dir_name)

                if '$RECYCLE.BIN' in full_path or 'System Volume Information' in full_path:
                    continue
                    
                path = full_path[len(root_path):].replace('\\','/')  # 디스크명 제거
                last_modified = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                
                data = (
                    current_id, volume_name, 'D', path, None, dir_name, parent_dir_name, None, None, None, None, last_modified, parent_pid, parent_pid
                )
                insert_to_db(cursor, data)
                parent_pid = current_id  # 현재 디렉터리 ID를 부모로 설정
                current_id += 1  # ID 증가

            # 파일 처리
            for file_name in files:
                full_path = os.path.join(current_path, file_name)
                if '$RECYCLE.BIN' in full_path or 'System Volume Information' in full_path:
                    continue                
                path = full_path[len(root_path):].replace('\\','/')  # 디스크명 제거
                name, extension = os.path.splitext(file_name)
                extension = extension.lstrip('.')  # 확장자 앞의 '.' 제거
                size = os.path.getsize(full_path)
                last_modified = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                search_key = generate_srch_key(file_name)
                data = (
                    current_id, volume_name, 'F', path, name, file_name, parent_dir_name, extension, size, None, search_key, last_modified, parent_pid, parent_pid
                )
                insert_to_db(cursor, data)
                current_id += 1  # ID 증가

        # 변경사항 저장
        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python hdd.py [DRIVE_LETTER] [VOLUME_NAME]")
        sys.exit(1)

    drive_letter = sys.argv[1].strip(':')
    volume_name = sys.argv[2]

    if len(drive_letter) != 1 or not drive_letter.isalpha():
        print("Invalid drive letter. Example: C or D")
        sys.exit(1)

    root_path = f"{drive_letter}:/"

    try:
        # 볼륨명을 명령행 인자로 받음
        print(f"Drive Letter: {drive_letter}")
        print(f"Volume Name: {volume_name}")
        scan_directory(root_path, volume_name)
        print("Done!!!")
    except Exception as e:
        print(f"Error: {e}")
