#!/bin/bash
# .env 파일의 절대 경로 지정
BASE_PATH="/c/Users/deHong/Documents/kdy/python-practice/diary-to-html"
ENV_PATH="${BASE_PATH}/.env"
SCRIPT="${BASE_PATH}/diary_to_html.py"
VENV_PATH="${BASE_PATH}/venv" # 가상 환경 경로 추가

# 인자 검증
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <OUTPUT_FILE> <FROM_DATE> <TO_DATE>"
    echo "Example: $0 202311.html 20220101 20230131"
    exit 1
fi

# 인자 설정
OUTPUT_FILE=$1
FROM_DATE=$2
TO_DATE=$3

# 가상 환경 활성화
source "${VENV_PATH}/Scripts/activate"

# .env 파일 로드
if [ -f "$ENV_PATH" ]; then
    echo ".env 활성화"
    export $(cat "$ENV_PATH" | xargs)
else
    echo ".env file not found in $ENV_PATH"
    exit 1
fi

# 입력된 인자 확인
echo "OUTPUT_FILE: $OUTPUT_FILE"
echo "FROM_DATE: $FROM_DATE"
echo "TO_DATE: $TO_DATE"

# Python 스크립트 실행
python "$SCRIPT" "$OUTPUT_FILE" "$FROM_DATE" "$TO_DATE"

# 실행 완료 메시지
echo "Diary to HTML conversion completed. Output file: $OUTPUT_FILE"
