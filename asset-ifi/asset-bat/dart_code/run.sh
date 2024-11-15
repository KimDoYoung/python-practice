#!/bin/bash 

PRG_NAME="dart_code"
current_date=$(date +"%Y_%m_%d")

# 로그 디렉터리 생성
mkdir -p "../logs/$PRG_NAME"
log_file="../logs/$PRG_NAME/${PRG_NAME}_${current_date}.log"

# 운영 체제 확인
OS_TYPE=$(uname)

# 프로젝트 루트 경로를 설정
PROJECT_ROOT=$(realpath "$(dirname "$0")/..")
echo "Project Root: [$PROJECT_ROOT]"
echo "OS TYPE: $OS_TYPE"
echo "Log File: $log_file"

if [[ "$OS_TYPE" == "Linux" || "$OS_TYPE" == "Darwin" ]]; then
    
    export ASSET_BAT_MODE="real"
    
    # 가상 환경 활성화 (Linux/macOS)
    source "$PROJECT_ROOT/env/bin/activate"
    
    # PYTHONPATH 설정
    export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
    
    # Python 스크립트 실행 및 로그 파일에 저장
    python "$PROJECT_ROOT/$PRG_NAME/main.py" >> "$log_file" 2>&1
    
    # 가상 환경 비활성화
    deactivate

elif [[ "$OS_TYPE" == "MINGW"* || "$OS_TYPE" == "CYGWIN"* ]]; then
    export ASSET_BAT_MODE="local"
    
    # 가상 환경 활성화 (Windows)
    source "$PROJECT_ROOT/env/Scripts/activate"
    
    # PYTHONPATH 설정
    export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
    echo "PYTHONPATH is set to: $PYTHONPATH"
    # Python 스크립트 실행 및 로그 파일에 저장
    $PROJECT_ROOT/env/Scripts/python "$PROJECT_ROOT/$PRG_NAME/main.py" >> "$log_file" 2>&1
    
    # 가상 환경 비활성화
    # 가상 환경 비활성화 (.bat 파일 실행)
    if [[ -f "$PROJECT_ROOT/env/Scripts/deactivate.bat" ]]; then
        cmd.exe /c "$PROJECT_ROOT/env/Scripts/deactivate.bat"
    else
        echo "Warning: Could not find deactivate script."
    fi
else
    echo "Unsupported Operating System: $OS_TYPE"
    exit 1
fi
