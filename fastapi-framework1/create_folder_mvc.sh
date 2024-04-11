#! /bin/bash
echo "----------------------------------------"
echo "MVC style folder structure"
echo "----------------------------------------"
mkdir -p .vscode
touch README.md
touch .vscode/settings.json
touch .vscode/launch.json
touch .gitignore

mkdir -p api/v1
mkdir -p core
mkdir -p models
mkdir -p services
mkdir -p static/js
mkdir -p static/css
mkdir -p static/image
mkdir -p templates

touch api/v1/home_routes.py
touch core/config.py
touch core/database.py
touch core/exceptions.py
touch core/logger.py
touch core/template_engine.py
touch core/util.py