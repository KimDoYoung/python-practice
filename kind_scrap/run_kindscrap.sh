#!/bin/bash

# 외부 실행 스크립트
# 사용법: ./run_kindscrap.sh <start_day> <end_day> <page_index>

start_day=$1
end_day=$2
page_index=$3

# 인자 확인
if [ -z "$start_day" ] || [ -z "$end_day" ] || [ -z "$page_index" ]; then
  echo "Usage: $0 <start_day> <end_day> <page_index>"
  echo "\texample: $0 2024-12-15 2024-12-31 all"
  exit 1
fi

# Docker 컨테이너 실행 명령
docker exec -it kindscrap_app python kindscrap.py "$start_day" "$end_day" "$page_index"
