#! /bin/bash
echo "----------------------------------------"
echo "MVC style folder structure"
echo "----------------------------------------"
mkdir -p core 
mkdir -p api/v1
mkdir -p model
mkdir -p db
mkdir -p service
mkdir -p static
mkdir -p template
#---------------------
mkdir -p static/css
mkdir -p static/js
mkdir -p static/image
mkdir -p db/schema


# files
touch README.md
touch main.py
touch static/css/style.css
touch static/js/scripts.js
touch api/v1/__init__.py
touch api/v1/routes.py
#touch api/v1/validators.py
#touch api/v1/exceptions.py
#touch api/v1/dependencies.py
#touch api/v1/deps.py
#touch api/v1/params.py
touch core/__init__.py
touch core/config.py
touch core/exception.py
touch core/logger.py
touch core/template_engine.py
#
touch db/db_access.py
touch model/base_model.py

#
touch db/schema/schema_base.py
