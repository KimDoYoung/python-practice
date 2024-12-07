import os
from datetime import datetime
from PIL import Image
import pymysql
from dotenv import load_dotenv

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

# 썸네일 저장 기본 경로
THUMB_BASE_DIR = "/home/kdy/uploaded/thumbs"


# 썸네일 생성 함수
def create_thumbnail(input_path, output_path, max_width=300):
    try:
        with Image.open(input_path) as img:
            # 원본 크기 가져오기
            width, height = img.size

            # 너비가 max_width보다 클 경우 비율에 맞게 조정
            if width > max_width:
                scale = max_width / width
                new_width = max_width
                new_height = int(height * scale)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # PNG로 저장
            img.save(output_path, format="PNG")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False
    return True


# DB에서 처리할 데이터 가져오기
def fetch_images_to_process():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT saved_dir_name, saved_file_name
            FROM ap_file
            WHERE thumb_path IS NULL
            AND content_type LIKE 'image%'
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    finally:
        connection.close()


# DB 업데이트 함수
def update_thumb_path(saved_dir_name, saved_file_name, thumb_path):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            query = """
            UPDATE ap_file
            SET thumb_path = %s
            WHERE saved_dir_name = %s AND saved_file_name = %s
            """
            cursor.execute(query, (thumb_path, saved_dir_name, saved_file_name))
            connection.commit()
    finally:
        connection.close()


# 메인 처리 함수
def process_thumbnails():
    rows = fetch_images_to_process()
    if not rows:
        print("No images to process.")
        return

    for saved_dir_name, saved_file_name in rows:
        input_path = os.path.join(saved_dir_name, saved_file_name)

        # 파일이 존재하는지 확인
        if not os.path.exists(input_path):
            print(f"File not found: {input_path}")
            continue

        # 이미지 생성일자 기반 폴더 생성
        file_date = datetime.fromtimestamp(os.path.getmtime(input_path))
        thumb_sub_dir = file_date.strftime("%Y%m")
        thumb_dir = os.path.join(THUMB_BASE_DIR, thumb_sub_dir)
        os.makedirs(thumb_dir, exist_ok=True)

        # 썸네일 저장 경로 생성
        thumb_name = os.path.splitext(saved_file_name)[0] + ".png"
        thumb_path = os.path.join(thumb_dir, thumb_name)

        # 썸네일 생성
        if create_thumbnail(input_path, thumb_path):
            print(f"Thumbnail created: {thumb_path}")
            # DB 업데이트
            update_thumb_path(saved_dir_name, saved_file_name, thumb_path)
        else:
            print(f"Failed to create thumbnail for: {input_path}")


# 실행
if __name__ == "__main__":
    process_thumbnails()
