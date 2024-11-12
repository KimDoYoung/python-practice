#!/bin/bash

# 가상 환경 활성화
source ../env/bin/activate

# 날짜 형식 정의 (yyyy_mm_dd)
current_date=$(date +"%Y_%m_%d")

# 로그 디렉터리 생성
mkdir -p ../log/fetch_ipo_data

# 로그 파일 경로 설정 (날짜 포함)
log_file="../log/fetch_ipo_data/fetch_ipo_data_${current_date}.log"

# Python 스크립트 실행 및 로그 파일에 append 모드로 저장
python main.py >> "$log_file" 2>&1

# 가상 환경 비활성화
deactivate
