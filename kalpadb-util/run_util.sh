#!/bin/bash

# 실행할 유틸리티 디렉토리 설정
UTIL_DIR=$1
shift  # 첫 번째 인자를 제거하여 나머지 인자를 처리 가능하게 만듦

if [ -z "$UTIL_DIR" ]; then
  echo "사용법: ./run_util.sh <유틸리티_폴더> [추가 인자...]"
  exit 1
fi

# 추가 인자 처리
ARGS="$@"

# Docker 실행 명령
docker exec -it kalpadb-util bash -c "
cd /app/$UTIL_DIR && \
python3 ${UTIL_DIR}.py $ARGS
"
