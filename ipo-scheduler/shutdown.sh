#!/bin/bash

# 변수 지정
# ----------------------------------------------------
PROJECT_NAME="ipo-scheduler"
# ----------------------------------------------------

# main.py 절대 경로 지정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${SCRIPT_DIR}/${PROJECT_NAME}_pid.txt"

# PID 파일이 있는지 확인
if [[ -f "$PID_FILE" ]]; then
    # PID 파일에서 PID 읽기
    PID=$(cat "$PID_FILE")
    
    # OS 확인
    OS=$(uname)

    # 운영체제별 프로세스 종료
    if [[ "$OS" == "Linux" ]]; then
        # Linux에서 PID로 프로세스 종료
        kill "$PID" && echo "SUCCESS: PID $PID 프로세스가 종료되었습니다."
    elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "MSYS"* ]]; then
        # Windows에서 PID로 프로세스 종료
        taskkill //PID "$PID" //F && echo "SUCCESS: PID $PID 프로세스가 종료되었습니다."
    else
        echo "지원하지 않는 운영체제입니다: $OS"
        exit 1
    fi

    # 종료 후 PID 파일 삭제
    rm "$PID_FILE"
    echo "${PROJECT_NAME} 서버가 종료되었습니다."
else
    echo "ERROR: PID 파일을 찾을 수 없습니다. 서버가 실행 중이 아닐 수 있습니다."
fi
