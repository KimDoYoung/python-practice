#!/bin/bash

# 변수 지정
# ----------------------------------------------------
PROJECT_NAME="kalpadb-api"
PROFILE="local"
# ----------------------------------------------------

# OS 확인
OS=$(uname)

# 운영체제별 가상환경 활성화
if [[ "$OS" == "Linux" ]]; then
    # Linux용 가상환경 활성화
    source ./env/bin/activate
elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "MSYS"* ]]; then
    # Windows(Git Bash)용 가상환경 활성화
    source ./env/Scripts/activate
else
    echo "지원하지 않는 운영체제입니다: $OS"
    exit 1
fi

# PYTHONPATH 설정
export PYTHONPATH=$(pwd)

# MODE 환경변수 설정
export KALPADB_API_MODE="$PROFILE"

# main.py 절대 경로 지정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_PY="$SCRIPT_DIR/app/${PROJECT_NAME}-main.py"

# FastAPI 서버 시작 (백그라운드 실행)
python "$MAIN_PY" &

# 백그라운드 PID를 Windows와 Linux에서 기록하는 방식
if [[ "$OS" == "Linux" ]]; then
    # Linux에서 백그라운드 PID 기록
    echo $! > "${SCRIPT_DIR}/${PROJECT_NAME}_pid.txt"
elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "MSYS"* ]]; then
    # Windows에서 정확히 python.exe와 "${PROJECT_NAME}-main.py"가 포함된 프로세스 PID 찾기
    sleep 1  # 프로세스가 시작될 때까지 잠시 대기
    wmic process where "commandline like '%python.exe%${PROJECT_NAME}-main.py%'" get processid | grep -Eo '[0-9]+' | sed '/^$/d' | head -n 1 > "${SCRIPT_DIR}/${PROJECT_NAME}_pid.txt"
fi

echo "${PROJECT_NAME} 서버가 시작되었습니다."
