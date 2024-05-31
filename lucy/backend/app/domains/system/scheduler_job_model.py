from datetime import datetime
from typing import Any, List, Optional
from beanie import Document
from pydantic import BaseModel

class JobBase(BaseModel):
    job_id: str
    job_name: str
    job_type: str  # 'system' 또는 'user'
    run_type: str  # 'cron' 또는 'date'
    func_name: str
    args: List[Any] = []  # 기본값을 빈 리스트로 설정
    cron: Optional[str] = None
    run_date: Optional[datetime] = None

class JobRequest(JobBase):
    pass

class SchedulerJob(Document, JobBase):
    class Settings:
        collection = "SchedulerJob"        


# {
#     "task_name": "scheduled_task",
#     "run_type": "cron",
#     "cron": "*/5 * * * *",
#     "job_id": "job_1",
#     "args": ["Hello, World!"]
# }

# {
#     "task_name": "scheduled_task",
#     "run_type": "date",
#     "run_date": "2024-06-01T12:30:00",
#     "job_id": "one_time_job_1",
#     "args": ["Hello, World!"]
# }
