from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel

class JobRequest(BaseModel):
    task_name: str
    job_id: str
    args: List[Any]
    run_type: str # cron, date
    cron: Optional[str] = None
    run_date: Optional[datetime] = None


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
