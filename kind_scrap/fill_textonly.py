import sqlite3
import sys
from bs4 import BeautifulSoup

def add_textonly_column(database_path):
    try:
        # SQLite 데이터베이스 연결
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # 'textonly' 컬럼이 없으면 추가
        cursor.execute("PRAGMA table_info(kind_ca)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'textonly' not in columns:
            cursor.execute("ALTER TABLE kind_ca ADD COLUMN textonly TEXT")
            print("'textonly' 컬럼이 추가되었습니다.")
        else:
            print("'textonly' 컬럼이 이미 존재합니다.")

        # 'content' 필드의 HTML에서 텍스트 추출
        cursor.execute("SELECT cd, content FROM kind_ca")
        rows = cursor.fetchall()

        for row in rows:
            cd = row[0]
            html_content = row[1]
            if html_content is not None:
                # HTML에서 텍스트 추출
                text_only = BeautifulSoup(html_content, 'html.parser').get_text(strip=True)
                cleaned_text = " ".join(text_only.split())
                # 'textonly' 컬럼에 업데이트
                cursor.execute("UPDATE kind_ca SET textonly = ? WHERE cd = ?", (cleaned_text, cd))
                print(f"Record {cd}의 'textonly' 컬럼이 업데이트되었습니다.")

        # 변경 사항 저장
        conn.commit()
        print("모든 레코드가 업데이트되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        # 데이터베이스 연결 닫기
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python fill_textonly.py <SQLite3 파일 경로>")
        sys.exit(1)

    database_path = sys.argv[1]
    add_textonly_column(database_path)
