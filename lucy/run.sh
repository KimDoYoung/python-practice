#!/bin/bash

# 가상환경 활성화 (Windows에서는 Scripts 폴더 사용)
source env/Scripts/activate

# PYTHONPATH에 backend 디렉터리 추가
export PYTHONPATH=$(pwd)

# main.py 파일 실행
echo "FastAPI 서버를 실행합니다..."
python "$(pwd)/backend/main.py"

# 실행이 끝난 후 가상환경 비활성화
deactivate
