#!/bin/bash

# 외부 실행 스크립트
# 사용법: ./run_kindscrap.sh <start_day> <end_day> <page_index>

sqlite3_db_file_name=$1


# 인자 확인
if [ -z "$sqlite3_db_file_name" ] ; then
  echo "Usage: $0 <sqlite3_db_file_name>"
  echo "\texample: $0 kindscrap_20241214_20241214.sqlite3"
  exit 1
fi

# Docker 컨테이너 실행 명령
docker exec -it kindscrap_app python fill_textonly.py "$sqlite3_db_file_name"
