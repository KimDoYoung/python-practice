import sys
from bs4 import BeautifulSoup

def extract_text_from_html(html_file):
    try:
        # HTML 파일 열기
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')

        # 텍스트 추출
        text_only = soup.get_text(strip=True)

        # 줄바꿈/다중 공백 정리
        cleaned_text = "\n".join(text_only.split())

        # 출력 파일 이름 생성 (확장자 변경)
        txt_file = html_file.rsplit('.', 1)[0] + '.txt'

        # 텍스트 저장
        with open(txt_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"텍스트가 추출되어 '{txt_file}'에 저장되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python extract_text.py <HTML 파일명>")
        sys.exit(1)

    html_file = sys.argv[1]
    extract_text_from_html(html_file)
