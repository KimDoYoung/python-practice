# Define your scheduled tasks
from backend.app.background.jobs.judal_scrap_1 import scrap_judal
from backend.app.background.jobs.site38 import site38_work


def test_task(message : str):
    print("테스트 스케줄러 " + message)

# Create a dictionary to map task names to functions
task_mapping = {
    "test_task": test_task,
    "scrap_judal": scrap_judal,
    "site38_work" : site38_work
}