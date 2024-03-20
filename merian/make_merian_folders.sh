#!/bin/bash

# 폴더 생성
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/app/api/endpoints
mkdir -p backend/app/core
mkdir -p backend/tests/test_api
mkdir -p backend/tests/test_models
mkdir -p frontend/static/css
mkdir -p frontend/static/js
mkdir -p frontend/static/images
mkdir -p frontend/templates/common
mkdir -p frontend/templates/pages
mkdir -p migrations

# 백엔드 필수 파일 생성
touch backend/app/models/user.py
touch backend/app/models/keyboard.py
touch backend/app/schemas/user_schema.py
touch backend/app/schemas/keyboard_schema.py
touch backend/app/services/user_service.py
touch backend/app/services/keyboard_service.py
touch backend/app/api/endpoints/user.py
touch backend/app/api/endpoints/keyboard.py
touch backend/app/core/config.py
touch backend/app/core/security.py
touch backend/main.py

# 테스트 파일 생성
touch backend/tests/test_api/test_user.py
touch backend/tests/test_api/test_keyboard.py
touch backend/tests/test_models/test_user.py
touch backend/tests/test_models/test_keyboard.py

# 프론트엔드 파일 생성
touch frontend/static/css/main.css
touch frontend/static/js/app.js
touch frontend/templates/common/header.html
touch frontend/templates/common/footer.html
touch frontend/templates/pages/login.html
touch frontend/templates/pages/list.html
touch frontend/templates/pages/insert.html
touch frontend/templates/pages/edit.html
touch frontend/index.html

# 기타 필수 파일 생성
touch .env
touch requirements.txt
touch README.md

echo "Project structure for 'merian' has been created."