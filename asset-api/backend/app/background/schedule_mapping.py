# schedule_mapping.py
"""
모듈 설명: 
    - 스케줄링 작업을 등록하는 파일
주요 기능:
    - job_mapping 딕셔너리에 스케줄링 작업을 등록

작성자: 김도영
작성일: 2024-11-05
버전: 1.0
"""# Define your scheduled tasks
from backend.app.background.jobs.job_shell import run_bash_shell
from backend.app.background.jobs.job_test import test_sync, test_async

# Create a dictionary to map task names to functions
job_mapping = {
    "test_sync": test_sync,
    "test_async": test_async,
    "run_bash_shell" : run_bash_shell,
#    "scrap_judal": scrap_judal,
    # "site38_work" : site38_work_main,
    # "site38_work" : site38_work,
    # "holiday_godata": fetch_and_upsert_holiday,
    # "fill_ls_stk_info": call_master_api_fill_ls_stk_info,
    # "judal_fetch" : judal_fetch
}