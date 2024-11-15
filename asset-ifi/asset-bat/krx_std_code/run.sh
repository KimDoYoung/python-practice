#!/bin/bash
current_date=$(date +"%Y_%m_%d")
PRG_NAME="krx_std_code"
PROJECT_ROOT=$(realpath "$(dirname "$0")/..")

# 로그 디렉터리 생성
mkdir -p "$PROJECT_ROOT/logs/$PRG_NAME"
log_file="$PROJECT_ROOT/logs/$PRG_NAME/${PRG_NAME}_${current_date}.log"

# 운영 체제 확인
OS_TYPE=$(uname)

echo "Project Root: [$PROJECT_ROOT]"
echo "OS TYPE: $OS_TYPE"
echo "Log File: $log_file"

if [[ "$OS_TYPE" == "Linux" || "$OS_TYPE" == "Darwin" ]]; then
    # 가상 환경 활성화 (Linux/macOS)
    export AssetBat_Mode="real"
    export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
    source $PROJECT_ROOT/env/bin/activate

    # Python 스크립트 실행 및 로그 파일에 저장
    $PROJECT_ROOT/env/Scripts/python "$PROJECT_ROOT/$PRG_NAME/main.py" >> "$log_file" 2>&1
    
    # 가상 환경 비활성화
    deactivate
else
    echo "Unsupported Operating System: $OS_TYPE"
    exit 1
fi
