import os
import pymysql
from PIL import Image

# DB 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),  # 기본 포트 3306
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4')  # 기본 문자셋 utf8mb4
}

def get_image_dimensions(file_path):
    """
    이미지 파일의 너비와 높이를 반환.
    :param file_path: 이미지 파일 경로
    :return: (width, height) 튜플
    """
    try:
        with Image.open(file_path) as img:
            return img.width, img.height
    except Exception as e:
        print(f"이미지 파일 처리 중 오류 발생: {file_path}, 오류: {e}")
        return None, None

def main():
    """
    ap_file 테이블의 이미지 파일의 width와 height를 업데이트.
    """
    connection = None
    try:
        # DB 연결
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # 조회 쿼리 실행
        select_query = """
            SELECT node_id, saved_dir_name, saved_file_name
            FROM ap_file
            WHERE content_type LIKE 'image%' AND width IS NULL  order by upload_dt desc limit 10;
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()

        for row in rows:
            node_id = row['node_id']
            saved_dir_name = row['saved_dir_name']
            saved_file_name = row['saved_file_name']

            # 물리적 파일 경로 생성
            file_path = os.path.join(saved_dir_name, saved_file_name)
            print(f"파일 경로: {file_path} node_id={node_id} width, height를 구하는 중입니다.")
            if not os.path.exists(file_path):
                print(f"파일이 존재하지 않음: {node_id} :  {file_path}")
                continue

            # 이미지 크기 가져오기
            width, height = get_image_dimensions(file_path)
            if width is None or height is None:
                print(f"이미지 크기 확인 실패: {file_path}")
                continue

            # 업데이트 쿼리 실행
            update_query = """
                UPDATE ap_file
                SET width = %s, height = %s
                WHERE node_id = %s;
            """
            cursor.execute(update_query, (width, height, node_id))
            print(f"업데이트 완료: node_id={node_id}, width={width}, height={height}")

        # 트랜잭션 커밋
        connection.commit()
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    main()
    print("완료")
