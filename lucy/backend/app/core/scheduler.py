# scheduler.py
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from typing import Any, Callable, Dict

class Scheduler:
    ''' 스케줄러 클래스 : singleton으로 동작 '''
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler()
            cls._instance.scheduler.start()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance    


    def add_cron_job(self, func: Callable, cron: str, job_id: str, args: tuple = ()) -> None:
        try:
            self.scheduler.add_job(func, CronTrigger.from_crontab(cron), id=job_id, args=args)
        except Exception as e:
            return {"error": str(e)}    

    def add_date_job(self, func: Callable, run_date: datetime, job_id: str, args: tuple = ()) -> None:
        try:
            self.scheduler.add_job(func, DateTrigger(run_date=run_date), id=job_id, args=args)
        except Exception as e:
            return {"error": str(e)}

    def get_jobs(self) -> Dict[str, Any]:
        jobs = self.scheduler.get_jobs()
        return [{"id": job.id, "name": job.name, "next_run_time": str(job.next_run_time)} for job in jobs]
    
    def remove_job(self, job_id: str):
        try:
            self.scheduler.remove_job(job_id)
            return {"message": "Job removed successfully"}
        except Exception as e:
            return {"error": str(e)}

    def shutdown(self):
        self.scheduler.shutdown()
