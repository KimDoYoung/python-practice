# Define your scheduled tasks
def test_task(message : str):
    print("테스트 스케줄러 " + message)

# Create a dictionary to map task names to functions
task_mapping = {
    "test_task": test_task
}