# template_engine.py
"""
모듈 설명: 
    - jinja2 템플릿 엔진을 사용하여 HTML 템플릿을 렌더링하는 모듈 
주요 기능:
    - render_template: 템플릿 파일을 렌더링하여 HTML 문자열을 반환

작성자: 김도영
작성일: 2024-07-18
버전: 1.0
"""
import os
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

# 프로젝트 루트 디렉토리를 기반으로 템플릿 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
template_dir = os.path.join(BASE_DIR, 'frontend', 'views')
logger.debug("------------------------------------------------")
logger.debug(f"template_dir: {template_dir}")
logger.debug("------------------------------------------------")
# Jinja2 환경 설정
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml']),
)

def render_template(template_name, context={}):
    template = env.get_template(template_name)
    return template.render(context)


def get_template_html(template_name):
    # 템플릿 로드
    template = env.get_template(template_name)
    template_str = template.render()  # 템플릿을 문자열로 렌더링

    # 정규 표현식을 사용하여 <body> 태그 안의 내용 추출
    if template_str.find('<body') != -1:
        body_content = re.search(r'<body[^>]*>(.*?)</body>', template_str, re.DOTALL).group(1)
    else:
        body_content = template_str
    return body_content.strip()
