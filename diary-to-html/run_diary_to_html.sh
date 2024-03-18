#!/bin/bash
# .env 파일의 절대 경로 지정
BASE_PATH="/c/Users/deHong/Documents/kdy/python-practice/diary-to-html"
ENV_PATH="${BASE_PATH}/.env"
SCRIPT="${BASE_PATH}/diary_to_html.py"
VENV_PATH="${BASE_PATH}/venv" # 가상 환경 경로 추가


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

# 오늘 날짜를 기준으로 변수 설정
TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE=$(date +%Y%m -d "$TODAY")".html"
FROM_DATE=$(date +%Y%m01 -d "$TODAY -1 year")
TO_DATE=$(date +%Y%m%d -d "$FROM_DATE +1 month -1 day")

echo "OUTPUT_FILE: $OUTPUT_FILE"
echo "FROM_DATE: $FROM_DATE"
echo "TO_DATE: $TO_DATE"

# Python 스크립트 실행
python $SCRIPT $OUTPUT_FILE $FROM_DATE $TO_DATE

# 실행 완료 메시지
echo "Diary to HTML conversion completed. Output file: $OUTPUT_FILE"
