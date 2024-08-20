# Define your scheduled tasks
from backend.app.background.jobs.fill_ls_stk_info import call_master_api_fill_ls_stk_info
from backend.app.background.jobs.job_test import simple_async_test, test1
from backend.app.background.jobs.site38 import site38_work
from backend.app.background.jobs.holiday_godata import fetch_and_upsert_holiday
from backend.app.background.jobs.judal_scrap_1 import judal_main as judal_fetch

# Create a dictionary to map task names to functions
job_mapping = {
    "test_task": test1,
    "simple_async_test": simple_async_test,
#    "scrap_judal": scrap_judal,
    # "site38_work" : site38_work_main,
    "site38_work" : site38_work,
    "holiday_godata": fetch_and_upsert_holiday,
    "fill_ls_stk_info": call_master_api_fill_ls_stk_info,
    "judal_fetch" : judal_fetch
}