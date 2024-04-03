#!/bin/bash

# 폴더 생성
mkdir -p backend/app/domains/user
mkdir -p backend/app/domains/stc/korea_investment
mkdir -p backend/app/api/v1/endpoints
mkdir -p backend/app/core/config
mkdir -p backend/tests/domains/user
mkdir -p backend/tests/api
mkdir -p frontend/public/css
mkdir -p frontend/public/js
mkdir -p frontend/public/images
mkdir -p frontend/views/common
mkdir -p frontend/views/pages
mkdir -p migrations
mkdir -p .docker
mkdir -p .github/workflows  # 예시로 GitHub Actions 사용

# 백엔드 필수 파일 생성
touch backend/app/domains/user/user_model.py
touch backend/app/domains/user/user_schema.py
touch backend/app/domains/user/user_service.py
touch backend/app/domains/stc/korea_investment/korea_investment_service.py
touch backend/app/api/v1/endpoints/user.py
touch backend/app/core/security.py
touch backend/app/core/config/development.py
touch backend/app/core/config/production.py
touch backend/main.py

# 테스트 파일 생성
touch backend/tests/domains/user/test_user.py
touch backend/tests/api/test_user.py
touch backend/tests/api/test_keyboard.py

# 프론트엔드 파일 생성
touch frontend/public/css/main.css
touch frontend/public/js/app.js
touch frontend/public/images/.gitkeep
touch frontend/views/common/header.html
touch frontend/views/common/footer.html
touch frontend/views/pages/login.html
touch frontend/views/pages/list.html
touch frontend/views/pages/insert.html
touch frontend/views/pages/edit.html
touch frontend/index.html

# Docker와 CI/CD 관련 파일 생성
touch .docker/Dockerfile
touch .docker/docker-compose.yml
touch .github/workflows/main.yml

# 기타 필수 파일 생성
touch .env
touch .env.development
touch .env.production
touch requirements.txt
touch README.md

echo "Enhanced project structure for 'joanna' has been created."
