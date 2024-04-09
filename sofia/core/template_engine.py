import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from core.logger import get_logger

logger = get_logger(__name__)

# 프로젝트 루트 디렉토리를 기반으로 템플릿 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(BASE_DIR, 'templates')
logger.debug("------------------------------------------------")
logger.debug(f"template_dir: {template_dir}")
logger.debug("------------------------------------------------")
# Jinja2 환경 설정
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml']),
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))'
)

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)
