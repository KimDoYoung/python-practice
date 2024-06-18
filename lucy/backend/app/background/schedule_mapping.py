# Define your scheduled tasks
from backend.app.background.jobs.job_test import simple_async_test, test1
from backend.app.background.jobs.site38 import site38_work



# Create a dictionary to map task names to functions
job_mapping = {
    "test_task": test1,
#    "scrap_judal": scrap_judal,
    # "site38_work" : site38_work_main,
    "site38_work" : site38_work,
    "simple_async_test": simple_async_test

}